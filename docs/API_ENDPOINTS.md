# API Endpoints - Fresh&Go

## CRM Service (Puerto 3001)

| Endpoint           | Método | Filtros                   | Descripción                            |
|------------------|--------|---------------------------|----------------------------------------|
| /clientes         | GET    | q, page, pageSize         | Obtener clientes                        |
| /clientes/:id     | GET    | -                         | Obtener cliente por ID                  |
| /pedidos          | GET    | clienteId, estado, page, pageSize | Obtener pedidos de un cliente          |
| /pedidos/:id      | GET    | -                         | Obtener pedido por ID                   |
| /proveedores      | GET    | -                         | Obtener proveedores                     |
| /proveedores/:id  | GET    | -                         | Obtener proveedor por ID                |
| /conductores      | GET    | disponibilidad            | Obtener conductores filtrando por disponibilidad |
| /conductores/:id  | GET    | -                         | Obtener conductor por ID                |

### Ejemplo de Uso

```bash
# Buscar clientes por nombre
curl "http://localhost:3001/clientes?q=hotel&page=1&pageSize=10"

# Obtener pedidos de un cliente
curl "http://localhost:3001/pedidos?clienteId=CLI001"
````

---

## IoT Service (Puerto 8001)

| Endpoint        | Método | Filtros                                               | Descripción                        |
| --------------- | ------ | ----------------------------------------------------- | ---------------------------------- |
| /sensores       | GET    | id, tipoProducto, ubicacionId                         | Obtener todos los sensores         |
| /sensores/{id}  | GET    | -                                                     | Obtener sensor específico por ID   |
| /lecturas       | GET    | sensorId, ubicacionId, from, to, estado, alertaActiva | Obtener lecturas de sensores       |
| /vehiculos      | GET    | -                                                     | Obtener todos los vehículos        |
| /vehiculos/{id} | GET    | -                                                     | Obtener vehículo específico por ID |

### Ejemplo de Uso

```bash
# Obtener sensores por tipo de producto
curl "http://localhost:8001/sensores?tipoProducto=refrigerado"

# Obtener lecturas filtrando por tiempo y estado
curl "http://localhost:8001/lecturas?sensorId=SENS001&from=2025-11-11T08:00:00Z&to=2025-11-11T09:00:00Z&estado=alerta"
```

---

## Códigos de Respuesta

| Código | Significado                                |
| ------ | ------------------------------------------ |
| 200    | OK - Solicitud exitosa                     |
| 201    | Created - Recurso creado                   |
| 400    | Bad Request - Parámetros inválidos         |
| 404    | Not Found - Recurso no encontrado          |
| 422    | Unprocessable Entity - Error de validación |
| 500    | Internal Server Error - Error del servidor |

### Formato de Error

```json
{
  "error": {
    "message": "Descripción del error",
    "statusCode": 404,
    "timestamp": "2025-11-11T12:34:56Z",
    "path": "/clientes/123",
    "method": "GET"
  }
}
```

---

> Nota:
>
> * En `/lecturas`, cada registro incluye temperatura, GPS, estado, alertaActiva y tiempoFueraRango.
> * En `/sensores`, `tipoProducto` indica refrigerado, congelado o delicado, y se incluye rango de temperatura y umbrales de alerta.

```
