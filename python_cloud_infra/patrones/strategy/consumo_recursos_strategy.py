"""
Modulo de la interfaz abstracta (Strategy) ConsumoRecursosStrategy.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

# Para type hints sin importacion circular
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio import Servicio

class ConsumoRecursosStrategy(ABC):
    """
    Interfaz (Strategy) para definir algoritmos intercambiables
    de consumo de potencia/recursos.

    Referencia: US-TECH-004, Rubrica 1.4
    """

    @abstractmethod
    def calcular_consumo(
        self,
        timestamp: datetime,
        servicio: 'Servicio'
    ) -> float:
        """
        Calcula la cantidad de potencia (MW) consumida por un servicio
        en funcion de la estrategia.

        Args:
            timestamp (datetime): La fecha y hora actual (para estrategias
                                  dinamicas basadas en la hora del dia).
            servicio (Servicio): El servicio que esta consumiendo potencia.

        Returns:
            float: La cantidad de potencia (MW) consumida.
        """
        pass