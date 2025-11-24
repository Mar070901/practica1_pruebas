/* 
======================================================================================
Nombre : routes/index.js
Descripción : Archivo que define los endpoints principales del servicio CRM Express.
Expone rutas para clientes, pedidos, proveedores y conductores. Cada endpoint usa 
controllers para la lógica de negocio y validadores AJV para verificar datos de entrada.

Detalle:
- GET /clientes
- GET /clientes/:id
- GET /pedidos
- GET /pedidos/:id
- GET /proveedores
- GET /proveedores/:id
- GET /conductores
- GET /conductores/:id

---------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      19-11-2025    Creación del módulo de rutas CRM
I002      JLC      19-11-2025    Añadido servicio CRM inicial (#3)
======================================================================================
*/

// Routes - Definición de endpoints
const express = require('express');
const router = express.Router();
const { AppError, asyncHandler } = require('../middleware/errorHandler');

module.exports = function(controllers, data, validator) {
  // CLIENTES
  router.get('/clientes', asyncHandler((req, res) => {
    const result = controllers.clientes.getAll(data, req.query, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  router.get('/clientes/:id', asyncHandler((req, res) => {
    const result = controllers.clientes.getById(data, req.params.id, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  // PEDIDOS
  router.get('/pedidos', asyncHandler((req, res) => {
    const result = controllers.pedidos.getAll(data, req.query, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  router.get('/pedidos/:id', asyncHandler((req, res) => {
    const result = controllers.pedidos.getById(data, req.params.id, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  // PROVEEDORES
  router.get('/proveedores', asyncHandler((req, res) => {
    const result = controllers.proveedores.getAll(data, req.query, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  router.get('/proveedores/:id', asyncHandler((req, res) => {
    const result = controllers.proveedores.getById(data, req.params.id, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  // CONDUCTORES
  router.get('/conductores', asyncHandler((req, res) => {
    const result = controllers.conductores.getAll(data, req.query, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  router.get('/conductores/:id', asyncHandler((req, res) => {
    const result = controllers.conductores.getById(data, req.params.id, validator);
    if (result.status) {
      throw new AppError(result.error, result.status);
    }
    res.json(result);
  }));

  return router;
};
