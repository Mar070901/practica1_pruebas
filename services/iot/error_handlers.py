/*
======================================================================================
Nombre      : error_handlers.py
Descripción : Manejo centralizado de excepciones para FastAPI. Centraliza la gestión
              de errores de validación, errores personalizados y errores no
              controlados. Incluye middleware para registro de errores.

--------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      20-11-2025    Creación inicial del módulo de manejo de errores
I002      JLC      20-11-2025    Integración con FastAPI y middleware de logging (#3)
======================================================================================
*\
    
"""
Manejo centralizado de excepciones para FastAPI
Centraliza la gestión de errores en toda la aplicación
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from typing import Optional
import logging
import traceback

# Configurar logging
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Clase base para errores de API personalizados"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()
        super().__init__(self.message)


class ValidationError(APIError):
    """Error de validación"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class NotFoundError(APIError):
    """Error de recurso no encontrado"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class BadRequestError(APIError):
    """Error de request malo"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


def setup_exception_handlers(app: FastAPI):
    """
    Configura todos los manejadores de excepciones centralizados
    """

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        """Manejador para errores de API personalizados"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "statusCode": exc.status_code,
                    "timestamp": exc.timestamp,
                    "path": str(request.url.path),
                    "method": request.method,
                    **({"details": exc.details} if exc.details else {})
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Manejador para errores de validación de FastAPI"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"][1:]),
                "type": error["type"],
                "message": error["msg"]
            })
        
        logger.warning(f"Validation error on {request.method} {request.url.path}: {errors}")
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "message": "Error de validación en los parámetros",
                    "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": str(request.url.path),
                    "method": request.method,
                    "details": errors
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Manejador general para excepciones no controladas"""
        timestamp = datetime.utcnow().isoformat()
        
        # Log del error
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path}",
            exc_info=True,
            extra={
                "timestamp": timestamp,
                "path": request.url.path,
                "method": request.method,
                "error": str(exc)
            }
        )
        
        # Respuesta al cliente
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "Error interno del servidor",
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "timestamp": timestamp,
                    "path": str(request.url.path),
                    "method": request.method
                }
            }
        )

    @app.middleware("http")
    async def error_logging_middleware(request: Request, call_next):
        """Middleware para loguear todas las requests y responses"""
        try:
            response = await call_next(request)
            
            # Log de response exitosa
            if response.status_code >= 400:
                logger.warning(
                    f"Response error: {request.method} {request.url.path} - {response.status_code}"
                )
            
            return response
            
        except Exception as exc:
            # Esta excepción será capturada por el exception_handler general
            raise

    return {
        "api_error_handler": api_error_handler,
        "validation_exception_handler": validation_exception_handler,
        "general_exception_handler": general_exception_handler,
        "error_logging_middleware": error_logging_middleware
    }
