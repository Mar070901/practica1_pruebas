/*
"""
======================================================================================
Nombre      : main.py
Descripción : Servicio principal FastAPI para el sistema IoT Fresh&Go. Gestiona 
              endpoints de sensores, lecturas, vehículos, dashboard y tracking 
              GPS, incluyendo validación de datos y filtros por parámetros.

--------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      24-11-2025    Creación inicial del main.py con endpoints básicos
I002      JLC      24-11-2025    Integración de filtros, validación JSON y estadísticas
I002      JLC      24-11-2025    Añadido endpoints GPS y dashboard resumen
======================================================================================
"""
*\

from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from dateutil import parser as date_parser
import jsonschema

app = FastAPI(
    title="IoT Fresh&Go - Monitoreo Cadena de Frío",
    version="2.0.0",
    description="Sistema de monitoreo de temperatura para garantizar la cadena de frío"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar schemas
def load_schema(filename: str):
    schema_path = Path(__file__).parent.parent.parent / "schemas" / filename
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

schemas = {
    'sensor': load_schema('sensor.schema.json'),
    'lectura': load_schema('lectura.schema.json'),
    'vehiculo': load_schema('vehiculo.schema.json')
}

# Cargar datos
def load_data(filename: str):
    data_path = Path(__file__).parent / "data" / filename
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

sensores = load_data('sensores.json')
lecturas = load_data('lecturas.json')
vehiculos = load_data('vehiculos.json')

# Función de validación
def validate_data(data, schema_name: str):
    try:
        jsonschema.validate(instance=data, schema=schemas[schema_name])
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Error de validación: {e}")
        return False

# ==================== SENSORES ====================

@app.get("/sensores")
async def get_sensores(
    tipo: Optional[str] = None,
    ubicacionId: Optional[str] = None,
    tipoAlimento: Optional[str] = Query(
        None, 
        description="Filtrar por tipo de alimento: congelado, refrigerado, no_refrigerado"
    )
):
    """
    Obtener listado de sensores
    
    Filtros disponibles:
    - tipo: Tipo de sensor (solo 'temperatura' disponible en v2.0)
    - ubicacionId: ID del vehículo o almacén
    - tipoAlimento: congelado, refrigerado, no_refrigerado
    """
    try:
        filtered = sensores
        
        if tipo:
            filtered = [s for s in filtered if s.get('tipo') == tipo]
        
        if ubicacionId:
            filtered = [s for s in filtered if s.get('ubicacionId') == ubicacionId]
        
        if tipoAlimento:
            filtered = [s for s in filtered if s.get('tipoAlimento') == tipoAlimento]
        
        # Validar cada sensor
        for sensor in filtered:
            if not validate_data(sensor, 'sensor'):
                raise HTTPException(
                    status_code=500,
                    detail=f"Sensor {sensor.get('id')} no cumple el schema"
                )
        
        return {
            "total": len(filtered),
            "data": filtered
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/sensores/{sensor_id}")
async def get_sensor(sensor_id: str):
    """Obtener un sensor específico por ID"""
    try:
        sensor = next((s for s in sensores if s['id'] == sensor_id), None)
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        if not validate_data(sensor, 'sensor'):
            raise HTTPException(
                status_code=500,
                detail="Datos no conformes con el schema"
            )
        
        return sensor
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# ==================== LECTURAS ====================

@app.get("/lecturas")
async def get_lecturas(
    sensorId: Optional[str] = None,
    ubicacionId: Optional[str] = None,
    estado: Optional[str] = Query(
        None,
        description="Filtrar por estado: normal, alerta, critico"
    ),
    cadenaRota: Optional[bool] = Query(
        None,
        description="Filtrar por rotura de cadena de frío"
    ),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Obtener lecturas de temperatura con detección de anomalías
    
    Filtros disponibles:
    - sensorId: ID del sensor
    - ubicacionId: ID de ubicación (vehículo/almacén)
    - estado: normal, alerta, critico
    - cadenaRota: true/false (cadena de frío rota)
    - from: Fecha inicio ISO 8601
    - to: Fecha fin ISO 8601
    - limit: Máximo de resultados (1-1000)
    """
    try:
        filtered = lecturas
        
        # Filtrar por sensorId
        if sensorId:
            filtered = [l for l in filtered if l.get('sensorId') == sensorId]
        
        # Filtrar por ubicacionId
        if ubicacionId:
            filtered = [l for l in filtered if l.get('ubicacionId') == ubicacionId]
        
        # Filtrar por estado
        if estado:
            filtered = [l for l in filtered if l.get('estado') == estado]
        
        # Filtrar por cadena rota
        if cadenaRota is not None:
            filtered = [l for l in filtered if l.get('cadenRota') == cadenaRota]
        
        # Parsear fechas si se proporcionan
        from_dt = None
        to_dt = None
        
        if from_date:
            try:
                from_dt = date_parser.isoparse(from_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha 'from' inválido. Use ISO 8601"
                )
        
        if to_date:
            try:
                to_dt = date_parser.isoparse(to_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha 'to' inválido. Use ISO 8601"
                )
        
        # Validar que from < to
        if from_dt and to_dt and from_dt > to_dt:
            raise HTTPException(
                status_code=400,
                detail="La fecha 'from' debe ser anterior a 'to'"
            )
        
        # Filtrar por rango de fechas
        if from_dt or to_dt:
            date_filtered = []
            for lectura in filtered:
                timestamp_str = lectura.get('timestamp')
                if timestamp_str:
                    timestamp = date_parser.isoparse(timestamp_str)
                    
                    if from_dt and timestamp < from_dt:
                        continue
                    if to_dt and timestamp > to_dt:
                        continue
                    
                    date_filtered.append(lectura)
            filtered = date_filtered
        
        # Aplicar límite
        filtered = filtered[:limit]
        
        # Validar cada lectura
        for lectura in filtered:
            if not validate_data(lectura, 'lectura'):
                raise HTTPException(
                    status_code=500,
                    detail=f"Lectura {lectura.get('id')} no cumple el schema"
                )
        
        # Calcular estadísticas
        total = len(filtered)
        alertas = len([l for l in filtered if l.get('estado') in ['alerta', 'critico']])
        criticas = len([l for l in filtered if l.get('estado') == 'critico'])
        cadenas_rotas = len([l for l in filtered if l.get('cadenRota') == True])
        
        return {
            "total": total,
            "limit": limit,
            "estadisticas": {
                "alertas": alertas,
                "criticas": criticas,
                "cadenas_rotas": cadenas_rotas,
                "porcentaje_normal": round((total - alertas) / total * 100, 2) if total > 0 else 0
            },
            "data": filtered
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/lecturas/alertas")
async def get_alertas_activas():
    """Obtener solo las lecturas con alertas activas"""
    try:
        alertas = [l for l in lecturas if l.get('alertaActiva') == True]
        
        # Validar
        for lectura in alertas:
            if not validate_data(lectura, 'lectura'):
                raise HTTPException(
                    status_code=500,
                    detail="Datos no conformes con el schema"
                )
        
        return {
            "total": len(alertas),
            "data": alertas
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/lecturas/cadena-rota")
async def get_cadenas_rotas():
    """Obtener lecturas donde se ha detectado rotura de cadena de frío"""
    try:
        rotas = [l for l in lecturas if l.get('cadenRota') == True]
        
        # Validar
        for lectura in rotas:
            if not validate_data(lectura, 'lectura'):
                raise HTTPException(
                    status_code=500,
                    detail="Datos no conformes con el schema"
                )
        
        # Agrupar por sensor
        por_sensor = {}
        for lectura in rotas:
            sensor_id = lectura.get('sensorId')
            if sensor_id not in por_sensor:
                por_sensor[sensor_id] = []
            por_sensor[sensor_id].append(lectura)
        
        return {
            "total": len(rotas),
            "sensores_afectados": len(por_sensor),
            "por_sensor": por_sensor,
            "data": rotas
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/lecturas/estadisticas/{ubicacion_id}")
async def get_estadisticas_ubicacion(ubicacion_id: str):
    """Obtener estadísticas de temperatura de una ubicación específica"""
    try:
        lecturas_ubicacion = [l for l in lecturas if l.get('ubicacionId') == ubicacion_id]
        
        if not lecturas_ubicacion:
            raise HTTPException(
                status_code=404,
                detail=f"No hay lecturas para la ubicación {ubicacion_id}"
            )
        
        # Calcular estadísticas
        temperaturas = [l.get('temperatura') for l in lecturas_ubicacion]
        
        estadisticas = {
            "ubicacionId": ubicacion_id,
            "total_lecturas": len(lecturas_ubicacion),
            "temperatura_promedio": round(sum(temperaturas) / len(temperaturas), 2),
            "temperatura_minima": min(temperaturas),
            "temperatura_maxima": max(temperaturas),
            "lecturas_normales": len([l for l in lecturas_ubicacion if l.get('estado') == 'normal']),
            "lecturas_alerta": len([l for l in lecturas_ubicacion if l.get('estado') == 'alerta']),
            "lecturas_criticas": len([l for l in lecturas_ubicacion if l.get('estado') == 'critico']),
            "cadena_rota": any([l.get('cadenRota') for l in lecturas_ubicacion]),
            "tiempo_max_fuera_rango": max([l.get('tiempoFueraRango', 0) for l in lecturas_ubicacion])
        }
        
        return estadisticas
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# ==================== VEHÍCULOS ====================

@app.get("/vehiculos")
async def get_vehiculos():
    """Obtener listado de vehículos"""
    try:
        for vehiculo in vehiculos:
            if not validate_data(vehiculo, 'vehiculo'):
                raise HTTPException(
                    status_code=500,
                    detail="Datos no conformes con el schema"
                )
        
        return {"data": vehiculos}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/vehiculos/{vehiculo_id}")
async def get_vehiculo(vehiculo_id: str):
    """Obtener un vehículo específico por ID"""
    try:
        vehiculo = next((v for v in vehiculos if v['id'] == vehiculo_id), None)
        
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        if not validate_data(vehiculo, 'vehiculo'):
            raise HTTPException(
                status_code=500,
                detail="Datos no conformes con el schema"
            )
        
        return vehiculo
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/vehiculos/{vehiculo_id}/estado-cadena")
async def get_estado_cadena_vehiculo(vehiculo_id: str):
    """
    Obtener el estado actual de la cadena de frío para un vehículo específico
    Incluye todas las zonas (sensores) del vehículo
    """
    try:
        # Verificar que el vehículo existe
        vehiculo = next((v for v in vehiculos if v['id'] == vehiculo_id), None)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Obtener sensores del vehículo
        sensores_vehiculo = [s for s in sensores if s.get('ubicacionId') == vehiculo_id]
        
        if not sensores_vehiculo:
            return {
                "vehiculoId": vehiculo_id,
                "matricula": vehiculo.get('matricula'),
                "estado_general": "sin_sensores",
                "zonas": []
            }
        
        zonas = []
        estado_general = "normal"
        
        for sensor in sensores_vehiculo:
            # Obtener última lectura del sensor
            lecturas_sensor = [l for l in lecturas if l.get('sensorId') == sensor['id']]
            if lecturas_sensor:
                # Ordenar por timestamp descendente
                lecturas_sensor.sort(key=lambda x: x.get('timestamp'), reverse=True)
                ultima_lectura = lecturas_sensor[0]
                
                zona_info = {
                    "sensorId": sensor['id'],
                    "nombre": sensor['nombre'],
                    "tipoProducto": sensor['tipoProducto'],
                    "rangoOptimo": f"{sensor['rangoMin']}°C - {sensor['rangoMax']}°C",
                    "temperaturaActual": ultima_lectura.get('temperatura'),
                    "estado": ultima_lectura.get('estado'),
                    "alertaActiva": ultima_lectura.get('alertaActiva'),
                    "tiempoFueraRango": ultima_lectura.get('tiempoFueraRango'),
                    "cadenRota": ultima_lectura.get('cadenRota'),
                    "ultimaActualizacion": ultima_lectura.get('timestamp')
                }
                
                zonas.append(zona_info)
                
                # Actualizar estado general
                if ultima_lectura.get('cadenRota'):
                    estado_general = "cadena_rota"
                elif ultima_lectura.get('estado') == 'critico' and estado_general != "cadena_rota":
                    estado_general = "critico"
                elif ultima_lectura.get('estado') == 'alerta' and estado_general not in ["critico", "cadena_rota"]:
                    estado_general = "alerta"
        
        return {
            "vehiculoId": vehiculo_id,
            "matricula": vehiculo.get('matricula'),
            "estado_general": estado_general,
            "total_zonas": len(zonas),
            "zonas_normal": len([z for z in zonas if z['estado'] == 'normal']),
            "zonas_alerta": len([z for z in zonas if z['estado'] == 'alerta']),
            "zonas_criticas": len([z for z in zonas if z['estado'] == 'critico']),
            "cadenas_rotas": len([z for z in zonas if z['cadenRota']]),
            "zonas": zonas
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# ==================== DASHBOARD / RESUMEN ====================
@app.get("/dashboard/resumen")
async def get_dashboard_resumen():
    """
    Obtener resumen general del sistema de monitoreo
    Ideal para dashboard de administración
    """
    try:
        # Contar sensores por tipo de alimento
        sensores_por_tipo = {}
        for sensor in sensores:
            tipo = sensor.get('tipoAlimento', 'desconocido')
            sensores_por_tipo[tipo] = sensores_por_tipo.get(tipo, 0) + 1
        
        # Analizar lecturas recientes (últimas de cada sensor)
        sensores_con_problemas = []
        sensores_normales = []
        
        for sensor in sensores:
            lecturas_sensor = [l for l in lecturas if l.get('sensorId') == sensor['id']]
            if lecturas_sensor:
                lecturas_sensor.sort(key=lambda x: x.get('timestamp'), reverse=True)
                ultima = lecturas_sensor[0]
                
                if ultima.get('cadenRota') or ultima.get('estado') in ['alerta', 'critico']:
                    sensores_con_problemas.append({
                        "sensorId": sensor['id'],
                        "nombre": sensor['nombre'],
                        "ubicacionId": sensor['ubicacionId'],
                        "tipoAlimento": sensor['tipoAlimento'],
                        "estado": ultima.get('estado'),
                        "temperatura": ultima.get('temperatura'),
                        "cadenRota": ultima.get('cadenRota')
                    })
                else:
                    sensores_normales.append(sensor['id'])
        
        # Contar ubicaciones afectadas
        ubicaciones_afectadas = set([s['ubicacionId'] for s in sensores_con_problemas])
        
        return {
            "timestamp_consulta": datetime.utcnow().isoformat() + "Z",
            "total_sensores": len(sensores),
            "sensores_por_tipo_alimento": sensores_por_tipo,
            "sensores_operativos": len(sensores_normales),
            "sensores_con_alertas": len(sensores_con_problemas),
            "ubicaciones_afectadas": len(ubicaciones_afectadas),
            "porcentaje_salud": round(len(sensores_normales) / len(sensores) * 100, 2) if len(sensores) > 0 else 0,
            "alertas_activas": sensores_con_problemas
        }
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# ==================== RUTA RAÍZ ====================
@app.get("/")
async def root():
    """Información del servicio IoT"""
    return {
        "servicio": "IoT Fresh&Go - Monitoreo de Temperatura",
        "version": "2.0.0",
        "descripcion": "Sistema de monitoreo de temperatura y GPS para alimentos",
        "categorias_alimentos": {
            "congelado": {
                "rango_optimo": "-18°C a -22°C",
                "umbral_alerta": "> -15°C",
                "umbral_critico": "> -12°C",
                "tiempo_maximo_fuera_rango": "15 minutos",
                "ejemplos": "Helados, carnes congeladas, pescado congelado"
            },
            "refrigerado": {
                "rango_optimo": "0°C - 4°C",
                "umbral_alerta": "> 4°C",
                "umbral_critico": "> 7°C",
                "tiempo_maximo_fuera_rango": "30 minutos",
                "ejemplos": "Lácteos, carnes frescas, verduras, frutas"
            },
            "no_refrigerado": {
                "rango_optimo": "15°C - 25°C",
                "umbral_alerta": "> 28°C",
                "umbral_critico": "> 32°C",
                "tiempo_maximo_fuera_rango": "Sin límite estricto",
                "ejemplos": "Conservas, pasta, arroz, legumbres secas, pan"
            }
        },
        "endpoints": [
            "GET /sensores",
            "GET /sensores/{id}",
            "GET /lecturas",
            "GET /lecturas/alertas",
            "GET /lecturas/cadena-rota",
            "GET /lecturas/estadisticas/{ubicacion_id}",
            "GET /lecturas/tracking/{ubicacion_id}",
            "GET /lecturas/mapa",
            "GET /vehiculos",
            "GET /vehiculos/{id}",
            "GET /vehiculos/{id}/estado-cadena",
            "GET /dashboard/resumen",
            "GET /docs - Documentación interactiva Swagger"
        ]
    }

# ==================== ENDPOINTS GPS ====================

@app.get("/lecturas/tracking/{ubicacion_id}")
async def get_tracking_ubicacion(
    ubicacion_id: str,
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Obtener el tracking (ruta GPS) de una ubicación específica
    Devuelve las coordenadas GPS de todas las lecturas para trazar la ruta
    """
    try:
        # Filtrar lecturas por ubicación
        lecturas_ubicacion = [l for l in lecturas if l.get('ubicacionId') == ubicacion_id]
        
        if not lecturas_ubicacion:
            raise HTTPException(
                status_code=404,
                detail=f"No hay lecturas para la ubicación {ubicacion_id}"
            )
        
        # Filtrar por fechas si se proporcionan
        from_dt = None
        to_dt = None
        
        if from_date:
            try:
                from_dt = date_parser.isoparse(from_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha 'from' inválido"
                )
        
        if to_date:
            try:
                to_dt = date_parser.isoparse(to_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha 'to' inválido"
                )
        
        if from_dt or to_dt:
            filtered = []
            for lectura in lecturas_ubicacion:
                timestamp = date_parser.isoparse(lectura.get('timestamp'))
                if from_dt and timestamp < from_dt:
                    continue
                if to_dt and timestamp > to_dt:
                    continue
                filtered.append(lectura)
            lecturas_ubicacion = filtered
        
        # Ordenar por timestamp
        lecturas_ubicacion.sort(key=lambda x: x.get('timestamp'))
        
        # Limitar resultados
        lecturas_ubicacion = lecturas_ubicacion[:limit]
        
        # Extraer información de tracking
        tracking_points = []
        for lectura in lecturas_ubicacion:
            gps = lectura.get('gps', {})
            tracking_points.append({
                "timestamp": lectura.get('timestamp'),
                "latitud": gps.get('latitud'),
                "longitud": gps.get('longitud'),
                "altitud": gps.get('altitud'),
                "temperatura": lectura.get('temperatura'),
                "estado": lectura.get('estado')
            })
        
        return {
            "ubicacionId": ubicacion_id,
            "total_puntos": len(tracking_points),
            "puntos": tracking_points
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/lecturas/mapa")
async def get_mapa_todas_ubicaciones():
    """
    Obtener la última posición GPS de todas las ubicaciones
    Útil para mostrar un mapa en tiempo real con todas las ubicaciones
    """
    try:
        # Obtener la última lectura de cada ubicación
        ubicaciones_map = {}
        
        for lectura in lecturas:
            ubicacion_id = lectura.get('ubicacionId')
            timestamp = lectura.get('timestamp')
            
            if ubicacion_id not in ubicaciones_map:
                ubicaciones_map[ubicacion_id] = lectura
            else:
                # Comparar timestamps y quedarse con el más reciente
                if timestamp > ubicaciones_map[ubicacion_id].get('timestamp'):
                    ubicaciones_map[ubicacion_id] = lectura
        
        # Formatear respuesta
        ubicaciones_actuales = []
        for ubicacion_id, lectura in ubicaciones_map.items():
            gps = lectura.get('gps', {})
            ubicaciones_actuales.append({
                "ubicacionId": ubicacion_id,
                "sensorId": lectura.get('sensorId'),
                "timestamp": lectura.get('timestamp'),
                "latitud": gps.get('latitud'),
                "longitud": gps.get('longitud'),
                "altitud": gps.get('altitud'),
                "temperatura": lectura.get('temperatura'),
                "estado": lectura.get('estado'),
                "alertaActiva": lectura.get('alertaActiva'),
                "cadenRota": lectura.get('cadenRota')
            })
        
        return {
            "total_ubicaciones": len(ubicaciones_actuales),
            "ubicaciones": ubicaciones_actuales
        }
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

