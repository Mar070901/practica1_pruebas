/* 
======================================================================================
Nombre : index.js
Descripción : Archivo de inicialización del servicio CRM Express. Configura la 
aplicación Express, carga módulos de data, controllers, rutas, schemas de validación 
con AJV, y centraliza el manejo de errores.

Detalle:
- Controllers: lógica del negocio en carpeta src/controllers
- Data: clientes, pedidos y productos en JSON
- Routes: endpoints en src/routes
- Middleware: manejo centralizado de errores en src/middleware
- Inicialización: arranca servidor Express en el puerto 3001

---------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------- ------------- -----------------------------------------------------
I001      MQP       19-11-2025    Creación del servicio CRM base
I002      JLC       19-11-2025    Añadido servicio CRM inicial (#3)
======================================================================================
*/

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

// Importar módulos
const dataModule = require('./data');
const controllersModule = require('./controllers');
const setupRoutes = require('./routes');
const { errorHandler, notFoundHandler, AppError } = require('./middleware/errorHandler');

const app = express();
const PORT = 3001;

// Configurar AJV
const ajv = new Ajv({ allErrors: true, formats: { email: true } });

// Middleware
app.use(cors());
app.use(express.json());

// Cargar schemas
const schemas = {
  cliente: JSON.parse(fs.readFileSync(path.join(__dirname, '../../schemas/cliente.schema.json'), 'utf8')),
  pedido: JSON.parse(fs.readFileSync(path.join(__dirname, '../../schemas/pedido.schema.json'), 'utf8')),
  proveedor: JSON.parse(fs.readFileSync(path.join(__dirname, '../../schemas/proveedor.schema.json'), 'utf8')),
  conductor: JSON.parse(fs.readFileSync(path.join(__dirname, '../../schemas/conductor.schema.json'), 'utf8'))
};

// Compilar validadores
const validators = {
  cliente: ajv.compile(schemas.cliente),
  pedido: ajv.compile(schemas.pedido),
  proveedor: ajv.compile(schemas.proveedor),
  conductor: ajv.compile(schemas.conductor)
};

// ==================== USAR MÓDULOS ====================
const data = dataModule;
const controllers = controllersModule;
const apiRoutes = setupRoutes(controllers, data, validators);

app.use('/', apiRoutes);

// Ruta raíz
app.get('/', (req, res) => {
  res.json({
    servicio: 'CRM Fresh&Go',
    version: '1.0.0',
    arquitectura: 'Modular (routes, controllers, data)',
    endpoints: [
      'GET /clientes',
      'GET /clientes/:id',
      'GET /pedidos',
      'GET /pedidos/:id',
      'GET /proveedores',
      'GET /proveedores/:id',
      'GET /conductores',
      'GET /conductores/:id'
    ]
  });
});

app.listen(PORT, () => {
  console.log(`CRM Service ejecutándose en http://localhost:${PORT}`);
  console.log(`Estructura: /data - /controllers - /routes`);
  console.log(`Middleware centralizado de errores activado`);
});

// Manejo centralizado de errores
app.use(notFoundHandler);
app.use(errorHandler);
