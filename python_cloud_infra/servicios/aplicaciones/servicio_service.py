"""
Modulo de la clase base abstracta ServicioService.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

# Imports para la inyeccion del Strategy (Patrón 4)
from python_cloud_infra.patrones.strategy.consumo_recursos_strategy import ConsumoRecursosStrategy

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio import Servicio


class ServicioService(ABC):
    """
    Clase base abstracta para todos los servicios de aplicaciones.
    
    Implementa la logica de negocio comun a todos los servicios,
    principalmente el consumo de recursos (potencia).
    
    Aqui se inyecta el patron Strategy (Rubrica 1.4, Rubrica Auto STRT-003).
    """

    def __init__(self, estrategia_consumo: ConsumoRecursosStrategy):
        """
        Inicializa el servicio inyectando la estrategia de consumo.

        Args:
            estrategia_consumo (ConsumoRecursosStrategy): La estrategia
                concreta (ej. Dinamico o Fijo) que este servicio usara.
        """
        self._estrategia_consumo: ConsumoRecursosStrategy = estrategia_consumo

    def consumir_recursos(self, servicio: 'Servicio') -> float:
        """
        Calcula y aplica el consumo de potencia a un servicio.
        
        Delega el calculo al patron Strategy inyectado.
        
        Args:
            servicio (Servicio): El servicio que va a consumir potencia.

        Returns:
            float: La cantidad de potencia (MW) que fue consumida.
        """
        # 1. Obtiene la fecha y hora actual (necesaria para nuestro Strategy)
        timestamp_actual = datetime.now()
        
        # 2. DELEGA el calculo al Strategy
        potencia_consumida = self._estrategia_consumo.calcular_consumo(
            timestamp=timestamp_actual,
            servicio=servicio
        )
        
        # 3. Aplica el resultado al servicio
        # (A diferencia de 'agua', la potencia no se acumula,
        # solo se 'setea' el consumo actual).
        servicio.set_potencia_consumida(potencia_consumida)
            
        return potencia_consumida

    @abstractmethod
    def mostrar_datos(self, servicio: 'Servicio') -> None:
        """
        Metodo abstracto para mostrar los datos especificos
        de cada tipo de servicio (US-009).
        
        Sera implementado por las clases hijas.

        Args:
            servicio (Servicio): El servicio a mostrar.
        """
        pass