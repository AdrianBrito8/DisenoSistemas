"""
Modulo de la clase base abstracta ServicioStatefulService.
Hereda de ServicioService.
"""
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_cloud_infra.servicios.aplicaciones.servicio_service import ServicioService
from python_cloud_infra.patrones.strategy.consumo_recursos_strategy import ConsumoRecursosStrategy

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
    from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch
    
    # TypeAlias para nuestros servicios Stateful
    ServicioStateful = ServicioDatabase | ServicioBatch


class ServicioStatefulService(ServicioService):
    """
    Clase base abstracta para servicios "Stateful" (Database, Batch).
    
    Hereda de ServicioService (reutilizando la inyeccion de Strategy
    y el metodo consumir_recursos).
    
    Añade un metodo abstracto 'escalar' que las clases hijas
    deben implementar (US-008).
    
    Referencia: Rubrica 2.2 (Jerarquia de Clases)
    """

    def __init__(self, estrategia_consumo: ConsumoRecursosStrategy):
        """
        Pasa la estrategia de consumo (que será Dinamica) a la clase base.
        """
        super().__init__(estrategia_consumo)

    @abstractmethod
    @override
    def mostrar_datos(self, servicio: 'ServicioStateful') -> None:
        """
        Metodo abstracto para mostrar datos (redefinido para Stateful).

        Args:
            servicio (ServicioStateful): El servicio (DB o Batch) a mostrar.
        """
        # Imprime la base comun a todos los servicios Stateful
        print(f"Servicio: {servicio.get_tipo()} (Stateful)")
        print(f"Espacio: {servicio.get_espacio_u()} U")
        print(f"Potencia (Actual): {servicio.get_potencia_consumida():.1f} MW")
        print(f"ID: {servicio.get_id()}")

    @abstractmethod
    def escalar(self, servicio: 'ServicioStateful') -> None:
        """
        Metodo abstracto para aplicar el escalado especifico
        (ej. +IOPS, +Workers) a un servicio Stateful.
        
        Esta lógica es DIFERENTE a la de PythonForestal (no es copia).
        
        Referencia: US-008

        Args:
            servicio (ServicioStateful): El servicio a escalar.
        """
        pass