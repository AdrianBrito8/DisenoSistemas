"""
Modulo del Enum TipoProceso.
"""
from enum import Enum

class TipoProceso(Enum):
    """
    Enumera los tipos de procesos batch permitidos para los
    ServiciosBatch.
    
    Referencia: US-005
    """
    ETL = "Extraccion, Transformacion y Carga"
    IA = "Entrenamiento de Inteligencia Artificial"
    REPORTING = "Generacion de Reportes"