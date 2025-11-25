
# Servicios Fresh&Go (Tema 2)

**Relacionado con:** I002 - Implementación de APIs simuladas (CRM e IoT) [#3]  - ID commit inicial: 88296c0

Este directorio contiene los servicios backend simulados del proyecto **Fresh&Go**, correspondientes al **Tema 2** de la práctica de Integración de Aplicaciones (IAAPS T2).
Se incluyen dos servicios independientes: **CRM** y **IoT**, que simulan la lógica de negocio, datos y endpoints definidos en los schemas del Tema 1.

---

##  Servicio CRM - I002: Añadido servicio CRM inicial #3 - ID Commit subida: 34f9519

* **Tecnología:** Node.js + Express
* **Objetivo:** Gestión simulada de clientes, pedidos, proveedores y conductores.
* **Estructura principal:**

  * `src/controllers`: lógica del negocio
  * `src/routes`: definición de endpoints
  * `src/middleware`: manejo de errores
  * `data`: datos JSON simulados de clientes, pedidos, productos y proveedores
  * `index.js`: inicialización del servicio
* **Endpoints principales:** `/clientes`, `/pedidos`, `/proveedores`, `/conductores`
* **Validación:** datos validados contra los schemas en `../../schemas/`

---

##  Servicio IoT - I002: Añadido servicio IoT inicial #3 - ID Commit subida: aabf890

* **Tecnología:** Python + FastAPI
* **Objetivo:** Monitoreo de vehículos refrigerados y sensores IoT.
* **Estructura principal:**

  * `controllers`: lógica del negocio
  * `routes`: definición de endpoints
  * `data`: sensores, lecturas y rutas en JSON
  * `error_handlers.py`: manejo de errores
  * `main.py`: inicialización del servicio
  * `requirements.txt`: librerías necesarias
* **Endpoints principales:** `/sensores`, `/lecturas`, `/vehiculos`
* **Validación:** datos validados contra los schemas en `../../schemas/`
* **Estados:** `activo`, `mantenimiento`, `inactivo`, `averia` para vehículos y `activo`, `inactivo`, `error` para sensores

---

## Uso general

1. **Instalar dependencias:**

```bash
# CRM
cd services/crm
npm install

# IoT
cd ../iot
pip install -r requirements.txt
```

2. **Ejecutar servicios:**

```bash
# CRM
npm run dev        # desarrollo
npm start          # producción

# IoT
uvicorn main:app --reload --port 8001
```

3. **Endpoints:** consultar documentación en cada servicio y validar contra schemas JSON en `../../schemas/`

---

## Contribución

* Hacer fork del repositorio
* Crear una rama para cada característica
* Hacer commit de los cambios referenciando el Issue [#3]
* Enviar Pull Request

---

## Licencia

MIT License - ver LICENSE para más detalles

---
