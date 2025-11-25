/*
"""
======================================================================================
Nombre      : data/__init__.py
Descripción : Módulo encargado de cargar los datos base del servicio IoT desde
              archivos JSON. Proporciona las listas de sensores, lecturas y 
              vehículos utilizadas por los controladores.

Detalle:
- sensores.json   → Datos de sensores físicos instalados
- lecturas.json   → Registros de medidas recolectadas
- vehiculos.json  → Datos de vehículos asociados a transporte y logística

--------------------------------------------------------------------------
HISTÓRICO DE CAMBIOS
ISSUE     AUTOR    FECHA         DESCRIPCIÓN
--------  -------  ------------  -----------------------------------------------------
I002      MQP      22-11-2025    Carga inicial de datos IoT desde JSON (#3)
I002      JLC      22-11-2025    Ajuste de rutas y compatibilidad UTF-8-SIG
======================================================================================
"""
*\

"""DATA - Carga de datos desde JSON"""
import json
from pathlib import Path

sensores = json.load(open(Path(__file__).parent / '../data/sensores.json', encoding='utf-8-sig'))
lecturas = json.load(open(Path(__file__).parent / '../data/lecturas.json', encoding='utf-8-sig'))
vehiculos = json.load(open(Path(__file__).parent / '../data/vehiculos.json', encoding='utf-8-sig'))
