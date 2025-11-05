"""
Modulo de la implementacion "Dinamica" del Strategy.
"""
from datetime import datetime
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports de la interfaz Strategy
from python_cloud_infra.patrones.strategy.consumo_recursos_strategy import ConsumoRecursosStrategy

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio import Servicio

# Imports de Constantes
from python_cloud_infra import constantes as C

# --- Definición de Horas Pico (Nuestra Lógica de Negocio Única) ---
HORA_PICO_INICIO = 9  # 9:00 AM
HORA_PICO_FIN = 18 # 6:00 PM (la hora 18 son las 18:00-18:59, así que usamos < 18)


class ConsumoDinamicoStrategy(ConsumoRecursosStrategy):
    """
    Estrategia de consumo de potencia dinámica (para Servicios Stateful).

    Consume potencia (MW) basándose en la hora del día (horas pico vs valle).
    Esta lógica es original de este proyecto y no una copia de PythonForestal.

    - Horas Pico (9:00 - 17:59): Consume 5 MW
    - Horas Valle (Resto): Consume 2 MW

    Referencia: US-008, US-TECH-004
    """

    @override
    def calcular_consumo(
        self,
        timestamp: datetime,
        servicio: 'Servicio'
    ) -> float:
        """
        Calcula el consumo basandose en la hora del dia.

        Args:
            timestamp (datetime): La fecha y hora actual.
            servicio (Servicio): El servicio (no se usa aqui, pero lo pide la interfaz).

        Returns:
            float: Cantidad de potencia (MW) consumida.
        """
        hora_actual = timestamp.hour
        
        # --- Lógica de Negocio Única (no es copia) ---
        # Comprueba si la hora actual esta en el rango de oficina (horas pico)
        if HORA_PICO_INICIO <= hora_actual < HORA_PICO_FIN:
            # Es hora pico
            return C.CONSUMO_DINAMICO_ALTO # 5 MW
        else:
            # Es hora valle (noche, madrugada, fin de semana si quisieramos)
            return C.CONSUMO_DINAMICO_BAJO # 2 MW