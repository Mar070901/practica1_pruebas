/*
"""
======================================================================================
Nombre      : routes/__init__.py
Descripción : Definición de endpoints de la API IoT. Expone rutas para sensores,
              lecturas y vehículos. Se integra con los controladores y el sistema
              centralizado de manejo de errores.

--------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      22-11-2025    Creación inicial de las rutas del servicio IoT (#3)
I002      JLC      22-11-2025    Integración con controladores y validadores
======================================================================================
"""
*\

"""ROUTES - Definición de endpoints"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from controllers import SensorController, LecturaController, VehiculoController
from error_handlers import NotFoundError, ValidationError

def setup_routes(data, validator):
    router = APIRouter()
    
    @router.get("/sensores")
    async def get_sensores(tipo: Optional[str] = None, ubicacionId: Optional[str] = None):
        result = SensorController.get_all(data, tipo=tipo, ubicacionId=ubicacionId, validator=validator)
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 404:
                raise NotFoundError(result['error'])
            else:
                raise ValidationError(result['error'])
        return result

    @router.get("/sensores/{sensor_id}")
    async def get_sensor(sensor_id: str):
        result = SensorController.get_by_id(data, sensor_id, validator)
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 404:
                raise NotFoundError(result['error'])
            else:
                raise ValidationError(result['error'])
        return result

    @router.get("/lecturas")
    async def get_lecturas(
        sensorId: Optional[str] = None,
        ubicacionId: Optional[str] = None,
        from_date: Optional[str] = Query(None, alias="from"),
        to_date: Optional[str] = Query(None, alias="to"),
        limit: int = Query(100, ge=1, le=1000)
    ):
        result = LecturaController.get_all(data, sensorId=sensorId, ubicacionId=ubicacionId,
                                           from_date=from_date, to_date=to_date, limit=limit, validator=validator)
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 404:
                raise NotFoundError(result['error'])
            else:
                raise ValidationError(result['error'])
        return result

    @router.get("/vehiculos")
    async def get_vehiculos():
        result = VehiculoController.get_all(data, validator)
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 404:
                raise NotFoundError(result['error'])
            else:
                raise ValidationError(result['error'])
        return result

    @router.get("/vehiculos/{vehiculo_id}")
    async def get_vehiculo(vehiculo_id: str):
        result = VehiculoController.get_by_id(data, vehiculo_id, validator)
        if isinstance(result, dict) and 'status' in result:
            if result['status'] == 404:
                raise NotFoundError(result['error'])
            else:
                raise ValidationError(result['error'])
        return result

    return router
