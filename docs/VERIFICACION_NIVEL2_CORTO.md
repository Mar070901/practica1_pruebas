#  Verificación Nivel 2

## Requisitos Implementados

### 1.  Endpoints con Filtros

**CRM:** 8 endpoints con búsqueda y paginación
- `GET /clientes?q=nombre` - Búsqueda por nombre/email
- `GET /pedidos?clienteId=...&estado=...` - Filtrado por cliente y estado
- `GET /conductores?disponibilidad=...` - Filtrado por disponibilidad

**IoT:** 5 endpoints con filtros
- `GET /sensores?tipo=...&ubicacionId=...` - Filtrado por tipo y ubicación
- `GET /lecturas?sensorId=...&from=...&to=...&limit=...` - Filtrado por rango

### 2.  Validación de Datos

- Schemas JSON en `/schemas/` para cada entidad
- CRM: Validación con AJV (cliente, pedido, proveedor, conductor)
- IoT: Validación con jsonschema (sensor, lectura, vehículo)
- Rechazo de datos no válidos con error 422

### 3.  Manejo Centralizado de Errores

- **Express:** Middleware `errorHandler` + `asyncHandler`
- **FastAPI:** Exception handlers centralizados
- Respuestas consistentes con timestamp, path, method
- Logging automático de errores

### 4.  Estructura Modular

- `/data` - Carga datos desde JSON
- `/controllers` - Lógica de negocio
- `/routes` - Definición de endpoints
- `/middleware` (CRM) - Manejo de errores
- `/schemas` - Validación de datos

### 5.  CORS Habilitado

- CRM: `cors()` middleware
- IoT: `CORSMiddleware` en FastAPI
- Permite requests desde cualquier origen

---

## Datos Incluidos

| Servicio | Entidades | Registros |
|----------|-----------|-----------|
| **CRM** | Clientes, Pedidos, Proveedores, Conductores | 5 c., 10 p., 3 prov., 4 cond. |
| **IoT** | Sensores, Lecturas, Vehículos | 9 sensores, 6 lecturas, 6 vehículos |

---

## Pruebas Rápidas

```bash
# CRM - Buscar cliente
curl http://localhost:3001/clientes?q=Hotel

# IoT - Obtener sensores
curl http://localhost:8001/sensores

# Error 404
curl http://localhost:3001/clientes/NO-EXISTE

# Error 422 (IoT validación)
curl "http://localhost:8001/lecturas?limit=abc"
```
