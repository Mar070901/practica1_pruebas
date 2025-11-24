# Schemas Fresh&Go (Tema 2) 
## I002: Añadidos schemas iniciales #3 - ID Commit: 30a5a2f

**Relacionado con:** 
Esta carpeta contiene los **JSON Schemas** utilizados para validar los datos de los servicios **CRM** e **IoT** del proyecto **Fresh&Go**.

> Nota: Los schemas incluidos son los mismos que se definieron en la **Práctica 1** y ya están mergeados en `main`. Se utilizan para asegurar que los endpoints devuelvan datos conforme a las estructuras esperadas.

## Contenido

- `cliente.schema.json` – Validación de datos de clientes  
- `pedido.schema.json` – Validación de datos de pedidos  
- `producto.schema.json` – Validación de datos de productos  
- `proveedor.schema.json` – Validación de datos de proveedores  
- `vehiculo.schema.json` – Validación de datos de vehículos  
- `incidencia.schema.json` – Validación de incidencias o alertas  
- Otros schemas según el proyecto

## Uso

Los servicios **CRM** e **IoT** referencian estos schemas para validar la información enviada o recibida. No se conectan a bases de datos reales, solo se usan para pruebas y simulaciones.

