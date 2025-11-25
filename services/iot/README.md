# IoT Fresh&Go Service

Servicio de monitoreo IoT para vehículos refrigerados de Fresh&Go. Proporciona endpoints para gestionar sensores, lecturas de datos y estados de vehículos.

## Descripción

Este servicio backend está desarrollado con **FastAPI** y permite:

- Consultar información de sensores instalados en vehículos
- Obtener lecturas en tiempo real de temperatura, ubicación y humedad
- Monitorear el estado de los vehículos refrigerados
- Validar datos conforme a esquemas JSON definidos
- Generar alertas cuando se detectan anomalías

## Requisitos

- Python 3.8+
- Dependencias especificadas en `requirements.txt`

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd fresh-and-go/services/iot
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload --port 8001
```

La API estará disponible en `http://localhost:8001`

## Documentación de la API

### Recursos Disponibles

#### 1. **Sensores** (`/sensores`)
- `GET /sensores` - Obtener todos los sensores con filtros opcionales
  - Parámetros de query: `tipo`, `ubicacionId`
- `GET /sensores/{sensor_id}` - Obtener un sensor específico
- `POST /sensores` - Crear un nuevo sensor
- `PUT /sensores/{sensor_id}` - Actualizar un sensor
- `DELETE /sensores/{sensor_id}` - Eliminar un sensor

#### 2. **Lecturas** (`/lecturas`)
- `GET /lecturas` - Obtener todas las lecturas con filtros
  - Parámetros: `sensorId`, `ubicacionId`, `desde`, `hasta`
- `GET /lecturas/{lectura_id}` - Obtener una lectura específica
- `POST /lecturas` - Registrar una nueva lectura
- `GET /lecturas/vehiculo/{vehiculo_id}` - Obtener lecturas de un vehículo

#### 3. **Vehículos** (`/vehiculos`)
- `GET /vehiculos` - Obtener todos los vehículos
  - Parámetros: `estado`, `modelo`
- `GET /vehiculos/{vehiculo_id}` - Obtener un vehículo específico
- `POST /vehiculos` - Crear un nuevo vehículo
- `PUT /vehiculos/{vehiculo_id}` - Actualizar un vehículo
- `DELETE /vehiculos/{vehiculo_id}` - Eliminar un vehículo
- `GET /vehiculos/{vehiculo_id}/estado` - Obtener estado actual del vehículo

## Estructura de Datos

### Sensor
```json
{
  "id": "SENS001",
  "tipo": "temperatura",
  "marca": "DHT22",
  "ubicacionId": "VEH001",
  "estado": "activo"
}
```

### Lectura
```json
{
  "id": "LECT001",
  "sensorId": "SENS001",
  "ubicacionId": "VEH001",
  "timestamp": "2025-10-31T08:00:00Z",
  "valor": 4.5,
  "unidad": "°C"
}
```

### Vehículo
```json
{
  "id": "VEH001",
  "placa": "ABC-123",
  "modelo": "Ford Transit",
  "año": 2023,
  "capacidad": 2500,
  "estado": "activo",
  "temperatura_optima_min": 2,
  "temperatura_optima_max": 8,
  "sensores": ["SENS001", "SENS002", "SENS003"]
}
```

## Validación

Los datos se validan contra esquemas JSON ubicados en `../../schemas/`:
- `sensor.schema.json`
- `lectura.schema.json`
- `vehiculo.schema.json`

## Estados Disponibles

### Vehículos
- `activo` - Operativo y monitoreado
- `mantenimiento` - En revisión
- `inactivo` - Fuera de servicio
- `averia` - Con problemas técnicos

### Sensores
- `activo` - Transmitiendo datos
- `inactivo` - No enviando lecturas
- `error` - Con mal funcionamiento

## Filtrado y Búsqueda

### Por tipo de sensor
```bash
GET /sensores?tipo=temperatura
```

### Por rango de fechas (lecturas)
```bash
GET /lecturas?desde=2025-10-31T00:00:00Z&hasta=2025-10-31T23:59:59Z
```

### Por ubicación
```bash
GET /lecturas?ubicacionId=VEH001
```

## Manejo de Errores

La API retorna códigos HTTP estándar:
- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado
- `400 Bad Request` - Datos inválidos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

Respuesta de error:
```json
{
  "detail": "Descripción del error"
}
```

## CORS

El servicio habilita CORS para todas las rutas, permitiendo acceso desde cualquier origen.

## Contribuir

Para contribuir al proyecto:
1. Hacer fork del repositorio
2. Crear una rama para la característica
3. Hacer commit de los cambios
4. Enviar un pull request

## Licencia

MIT License - Ver LICENSE para más detalles

## Autor

Fresh&Go Development Team

## Contacto

Para reportar issues o sugerencias, contactar al equipo de desarrollo.
