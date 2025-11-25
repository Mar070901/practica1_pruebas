# CRM Service - Fresh&Go

Servicio de gestión de clientes, pedidos, proveedores y conductores para la plataforma Fresh&Go.

## Descripción

Este servicio CRM está desarrollado con **Node.js** y **Express**.

## Tecnologías

- Node.js 18+
- Express.js
- AJV (JSON Schema)
- Nodemon (desarrollo)

## Instalación

```bash
npm install
```

## Ejecución

### Modo Desarrollo
```bash
npm run dev
```

### Modo Producción
```bash
npm start
```

El servicio estará disponible en: http://localhost:3001

## Endpoints

### Clientes
- GET /clientes - Listar clientes
- GET /clientes/:id - Obtener cliente
- POST /clientes - Crear cliente
- PUT /clientes/:id - Actualizar cliente
- DELETE /clientes/:id - Eliminar cliente

### Pedidos
- GET /pedidos - Listar pedidos
- GET /pedidos/:id - Obtener pedido

### Proveedores
- GET /proveedores - Listar proveedores

### Conductores
- GET /conductores - Listar conductores

## Validación

Los datos se validan contra JSON Schemas en /schemas/

