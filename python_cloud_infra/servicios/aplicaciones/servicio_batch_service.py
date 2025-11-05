"""
Modulo del servicio concreto ServicioBatchService.
"""
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_cloud_infra.servicios.aplicaciones.servicio_stateful_service import ServicioStatefulService

# Imports para inyectar el Strategy (Nuestra lógica de horas pico)
from python_cloud_infra.patrones.strategy.impl.consumo_dinamico_strategy import ConsumoDinamicoStrategy

# Imports para constantes
from python_cloud_infra import constantes as C

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch


class ServicioBatchService(ServicioStatefulService):
    """
    Servicio concreto para la logica de negocio de los ServiciosBatch.
    
    Hereda de ServicioStatefulService.
    Inyecta la estrategia de consumo dinamico (basado en horas pico).
    Implementa la logica de escalado de Workers.
    """

    def __init__(self):
        """
        Inicializa el ServicioBatchService.
        
        Inyecta la estrategia dinámica (la de horas pico).
        """
        # Inyecta la misma estrategia que Database
        super().__init__(ConsumoDinamicoStrategy())

    @override
    def mostrar_datos(self, servicio: 'ServicioBatch') -> None:
        """
        Muestra los datos especificos de un ServicioBatch.
        Implementacion de US-009.

        Args:
            servicio (ServicioBatch): La entidad Batch a mostrar.
        """
        # 1. Llama a la implementacion base de ServicioStatefulService
        #    (que imprime ID, Tipo, Potencia, Espacio)
        super().mostrar_datos(servicio)
        
        # 2. Imprime los datos especificos de Batch (nuestra lógica)
        print(f"Tipo Proceso: {servicio.get_tipo_proceso().name}")
        print(f"Workers (Actual): {servicio.get_workers()}")

    @override
    def escalar(self, servicio: 'ServicioBatch') -> None:
        """
        Implementa la logica de escalado para un Servicio Batch.
        Logica de negocio original de US-008 (no es copia).

        Args:
            servicio (ServicioBatch): El servicio de Batch a escalar.
        """
        workers_actuales = servicio.get_workers()
        nuevos_workers = workers_actuales + C.ESCALA_WORKERS_POR_ASIGNACION
        
        servicio.set_workers(nuevos_workers)
        
        print(f"    -> [Servicio {servicio.get_id()}] Escalado de Batch: Workers aumentados a {nuevos_workers}")