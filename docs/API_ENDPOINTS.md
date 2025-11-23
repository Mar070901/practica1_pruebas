#  API Endpoints - Fresh&Go

## CRM Service (Puerto 3001)

| Endpoint | Método | Filtros | Descripción |
|----------|--------|---------|------------|
| `/clientes` | GET | `q`, `page`, `pageSize` | Obtener clientes |
| `/clientes/:id` | GET | - | Obtener cliente por ID |
| `/pedidos` | GET | `clienteId`, `estado`, `page`, `pageSize` | Obtener pedidos |
| `/pedidos/:id` | GET | - | Obtener pedido por ID |
| `/proveedores` | GET | - | Obtener proveedores |
| `/proveedores/:id` | GET | - | Obtener proveedor por ID |
| `/conductores` | GET | `disponibilidad` | Obtener conductores |
| `/conductores/:id` | GET | - | Obtener conductor por ID |

### Ejemplo de Uso

```bash
# Buscar clientes por nombre
curl "http://localhost:3001/clientes?q=hotel&page=1&pageSize=10"

# Obtener pedidos de un cliente
curl "http://localhost:3001/pedidos?clienteId=CLI001"
```

---

## IoT Service (Puerto 8001)

| Endpoint | Método | Filtros | Descripción |
|----------|--------|---------|------------|
| `/sensores` | GET | `tipo`, `ubicacionId` | Obtener sensores |
| `/sensores/{id}` | GET | - | Obtener sensor por ID |
| `/lecturas` | GET | `sensorId`, `ubicacionId`, `from`, `to`, `limit` | Obtener lecturas |
| `/vehiculos` | GET | - | Obtener vehículos |
| `/vehiculos/{id}` | GET | - | Obtener vehículo por ID |

### Ejemplo de Uso

```bash
# Obtener sensores por tipo
curl "http://localhost:8001/sensores?tipo=RefrigerationTemp"

# Obtener lecturas con rango de fechas
curl "http://localhost:8001/lecturas?from=2025-10-31&to=2025-11-01&limit=50"
```

---

## Códigos de Respuesta

| Código | Significado |
|--------|------------|
| **200** | OK - Éxito |
| **400** | Bad Request - Parámetros inválidos |
| **404** | Not Found - Recurso no encontrado |
| **422** | Unprocessable Entity - Error de validación |
| **500** | Internal Server Error |

---

## Formato de Error

```json
{
  "error": {
    "message": "Descripción del error",
    "statusCode": 404,
    "timestamp": "2025-10-31T12:34:56Z",
    "path": "/clientes/123",
    "method": "GET"
  }
}
```

**Fecha:** 2025-10-31 | **Versión:** 1.0.0
