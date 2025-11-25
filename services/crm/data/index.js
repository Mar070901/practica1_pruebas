// Data layer - Carga de datos desde JSON
const fs = require('fs');
const path = require('path');

module.exports = {
  clientes: JSON.parse(fs.readFileSync(path.join(__dirname, '../data/clientes.json'), 'utf8')),
  pedidos: JSON.parse(fs.readFileSync(path.join(__dirname, '../data/pedidos.json'), 'utf8')),
  proveedores: JSON.parse(fs.readFileSync(path.join(__dirname, '../data/proveedores.json'), 'utf8')),
  conductores: JSON.parse(fs.readFileSync(path.join(__dirname, '../data/conductores.json'), 'utf8'))
};
