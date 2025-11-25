/* 
======================================================================================
Nombre : middleware/errorHandler.js
Descripción : Middleware centralizado para el manejo de errores en Express. Incluye una 
clase personalizada AppError, control de errores conocidos, validaciones JSON, 
validaciones AJV, rutas inexistentes y errores internos no controlados.

Detalle:
- Clase AppError(message, statusCode)
- errorHandler: middleware principal de errores
- notFoundHandler: captura rutas inexistentes
- asyncHandler: wrap para funciones async

---------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      19-11-2025    Creación del manejador de errores
I002      JLC      19-11-2025    Añadido servicio CRM inicial (#3)
======================================================================================
*/

/**
 * Middleware centralizado de manejo de errores para Express
 * Gestiona todos los errores de la aplicación en un único lugar
 */

// Clase personalizada para errores de aplicación
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.timestamp = new Date().toISOString();
    
    Error.captureStackTrace(this, this.constructor);
  }
}

// Middleware de manejo de errores
const errorHandler = (err, req, res, next) => {
  err.timestamp = new Date().toISOString();
  err.path = req.path;
  err.method = req.method;

  // Errores conocidos
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        message: err.message,
        statusCode: err.statusCode,
        timestamp: err.timestamp,
        path: err.path,
        method: err.method
      }
    });
  }

  // Error de validación JSON
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({
      error: {
        message: 'JSON inválido en el request',
        statusCode: 400,
        timestamp: err.timestamp,
        details: err.message,
        path: err.path,
        method: err.method
      }
    });
  }

  // Error de validación de esquema (AJV)
  if (err.validation) {
    return res.status(400).json({
      error: {
        message: 'Error de validación de esquema',
        statusCode: 400,
        timestamp: err.timestamp,
        details: err.validation,
        path: err.path,
        method: err.method
      }
    });
  }

  // Error de no encontrado
  if (err.statusCode === 404) {
    return res.status(404).json({
      error: {
        message: err.message || 'Recurso no encontrado',
        statusCode: 404,
        timestamp: err.timestamp,
        path: err.path,
        method: err.method
      }
    });
  }

  // Errores internos no controlados
  console.error('❌ Error no controlado:', {
    message: err.message,
    stack: err.stack,
    timestamp: err.timestamp,
    path: err.path,
    method: err.method
  });

  return res.status(err.statusCode || 500).json({
    error: {
      message: err.message || 'Error interno del servidor',
      statusCode: err.statusCode || 500,
      timestamp: err.timestamp,
      path: err.path,
      method: err.method,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
};

// Middleware para capturar rutas no encontradas
const notFoundHandler = (req, res, next) => {
  const error = new AppError(`Ruta no encontrada: ${req.path}`, 404);
  next(error);
};

// Función auxiliar para wrap de funciones async
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = {
  AppError,
  errorHandler,
  notFoundHandler,
  asyncHandler
};
