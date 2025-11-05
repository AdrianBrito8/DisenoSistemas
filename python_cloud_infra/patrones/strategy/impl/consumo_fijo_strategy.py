"""
Modulo de la implementacion "Fija" del Strategy.
"""
from datetime import datetime
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports de la interfaz Strategy
from python_cloud_infra.patrones.strategy.consumo_recursos_strategy import ConsumoRecursosStrategy

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio import Servicio


class ConsumoFijoStrategy(ConsumoRecursosStrategy):
    """
    Estrategia de consumo de potencia fija (para Servicios Stateless).

    Consume una cantidad constante de potencia (MW), definida en
    su constructor, independientemente de la hora o carga.

    Referencia: US-008, US-TECH-004
    """

    def __init__(self, cantidad_fija: float):
        """
        Inicializa la estrategia.

        Args:
            cantidad_fija (float): La cantidad fija de potencia (MW)
                                   que consumirá (ej. 1 MW o 2 MW).
        
        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if cantidad_fija < 0:
            raise ValueError("La cantidad fija de consumo no puede ser negativa")
        self._cantidad_mw: float = cantidad_fija

    @override
    def calcular_consumo(
        self,
        timestamp: datetime,
        servicio: 'Servicio'
    ) -> float:
        """
        Devuelve la cantidad fija definida en el constructor.

        Args:
            timestamp (datetime): No se usa en esta estrategia.
            servicio (Servicio): No se usa en esta estrategia.

        Returns:
            float: La cantidad de potencia (MW) consumida.
        """
        return self._cantidad_mw