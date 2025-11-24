/* 
======================================================================================
Nombre : controllers/index.js
Descripción : Módulo que contiene la lógica de negocio del servicio CRM Express. 
Incluye operaciones de lectura, filtrado y validación para clientes, pedidos,
proveedores y conductores.

Detalle:
- clientes.getAll(data, query, validator)
- clientes.getById(data, id, validator)
- pedidos.getAll(data, query, validator)
- pedidos.getById(data, id, validator)
- proveedores.getAll(data, query, validator)
- proveedores.getById(data, id, validator)
- conductores.getAll(data, query, validator)
- conductores.getById(data, id, validator)

---------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      20-11-2025    Creación del módulo de controllers
I002      JLC      20-11-2025    Añadido servicio CRM inicial (#3)
======================================================================================
*/

// Controllers - Lógica de negocio

module.exports = {
  clientes: {
    getAll(data, query, validator) {
      const { q, page = 1, pageSize = 25 } = query;
      const pageNum = parseInt(page);
      const pageSizeNum = Math.min(parseInt(pageSize), 100);
      
      if (isNaN(pageNum) || pageNum < 1 || isNaN(pageSizeNum) || pageSizeNum < 1) {
        return { error: 'Parámetros de paginación inválidos', status: 400 };
      }
      
      let filtered = data.clientes;
      if (q) {
        const search = q.toLowerCase();
        filtered = data.clientes.filter(c => 
          c.nombre.toLowerCase().includes(search) || 
          (c.email && c.email.toLowerCase().includes(search))
        );
      }
      
      const total = filtered.length;
      const start = (pageNum - 1) * pageSizeNum;
      const paginatedData = filtered.slice(start, start + pageSizeNum);
      
      for (const cliente of paginatedData) {
        if (!validator.cliente(cliente)) {
          return { error: 'Datos no conformes con el schema', status: 500 };
        }
      }
      
      return { total, page: pageNum, pageSize: pageSizeNum, data: paginatedData };
    },

    getById(data, id, validator) {
      const cliente = data.clientes.find(c => c.id === id);
      if (!cliente) return { error: 'Cliente no encontrado', status: 404 };
      if (!validator.cliente(cliente)) return { error: 'Datos no conformes con el schema', status: 500 };
      return cliente;
    }
  },

  pedidos: {
    getAll(data, query, validator) {
      const { clienteId, estado, page = 1, pageSize = 25 } = query;
      const pageNum = parseInt(page);
      const pageSizeNum = Math.min(parseInt(pageSize), 100);
      
      if (isNaN(pageNum) || pageNum < 1 || isNaN(pageSizeNum) || pageSizeNum < 1) {
        return { error: 'Parámetros de paginación inválidos', status: 400 };
      }
      
      let filtered = data.pedidos;
      if (clienteId) filtered = filtered.filter(p => p.clienteId === clienteId);
      if (estado) filtered = filtered.filter(p => p.estado === estado);
      
      const total = filtered.length;
      const start = (pageNum - 1) * pageSizeNum;
      const paginatedData = filtered.slice(start, start + pageSizeNum);
      
      for (const pedido of paginatedData) {
        if (!validator.pedido(pedido)) {
          return { error: 'Datos no conformes con el schema', status: 500 };
        }
      }
      
      return { total, page: pageNum, pageSize: pageSizeNum, data: paginatedData };
    },

    getById(data, id, validator) {
      const pedido = data.pedidos.find(p => p.id === id);
      if (!pedido) return { error: 'Pedido no encontrado', status: 404 };
      if (!validator.pedido(pedido)) return { error: 'Datos no conformes con el schema', status: 500 };
      return pedido;
    }
  },

  proveedores: {
    getAll(data, query, validator) {
      for (const proveedor of data.proveedores) {
        if (!validator.proveedor(proveedor)) {
          return { error: 'Datos no conformes con el schema', status: 500 };
        }
      }
      return { data: data.proveedores };
    },

    getById(data, id, validator) {
      const proveedor = data.proveedores.find(p => p.id === id);
      if (!proveedor) return { error: 'Proveedor no encontrado', status: 404 };
      if (!validator.proveedor(proveedor)) return { error: 'Datos no conformes con el schema', status: 500 };
      return proveedor;
    }
  },

  conductores: {
    getAll(data, query, validator) {
      const { disponibilidad } = query;
      let filtered = data.conductores;
      
      if (disponibilidad !== undefined) {
        const disponible = disponibilidad === 'true';
        filtered = data.conductores.filter(c => c.disponibilidad === disponible);
      }
      
      for (const conductor of filtered) {
        if (!validator.conductor(conductor)) {
          return { error: 'Datos no conformes con el schema', status: 500 };
        }
      }
      
      return { data: filtered };
    },

    getById(data, id, validator) {
      const conductor = data.conductores.find(c => c.id === id);
      if (!conductor) return { error: 'Conductor no encontrado', status: 404 };
      if (!validator.conductor(conductor)) return { error: 'Datos no conformes con el schema', status: 500 };
      return conductor;
    }
  }
};
