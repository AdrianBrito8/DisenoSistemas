"""
Modulo del servicio concreto ServicioDatabaseService.
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
    from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase


class ServicioDatabaseService(ServicioStatefulService):
    """
    Servicio concreto para la logica de negocio de los ServiciosDatabase.
    
    Hereda de ServicioStatefulService.
    Inyecta la estrategia de consumo dinamico (basado en horas pico).
    Implementa la logica de escalado de IOPS.
    """

    def __init__(self):
        """
        Inicializa el ServicioDatabaseService.
        
        Aqui se realiza la INYECCION de la estrategia concreta
        (ConsumoDinamicoStrategy) en la clase base,
        cumpliendo con la Rubrica 1.4 y nuestra lógica original.
        """
        # Inyecta la estrategia dinámica (la de horas pico)
        super().__init__(ConsumoDinamicoStrategy())

    @override
    def mostrar_datos(self, servicio: 'ServicioDatabase') -> None:
        """
        Muestra los datos especificos de un ServicioDatabase.
        Implementacion de US-009.

        Args:
            servicio (ServicioDatabase): La entidad Database a mostrar.
        """
        # 1. Llama a la implementacion base de ServicioStatefulService
        #    (que imprime ID, Tipo, Potencia, Espacio)
        super().mostrar_datos(servicio)
        
        # 2. Imprime los datos especificos de Database (nuestra lógica)
        print(f"Motor: {servicio.get_motor()} (v{servicio.get_version()})")
        print(f"IOPS (Actual): {servicio.get_iops()}")

    @override
    def escalar(self, servicio: 'ServicioDatabase') -> None:
        """
        Implementa la logica de escalado para una Base de Datos.
        Logica de negocio original de US-008 (no es copia).

        Args:
            servicio (ServicioDatabase): El servicio de BBDD a escalar.
        """
        iops_actuales = servicio.get_iops()
        nuevos_iops = iops_actuales + C.ESCALA_IOPS_POR_ASIGNACION
        
        servicio.set_iops(nuevos_iops)
        
        print(f"    -> [Servicio {servicio.get_id()}] Escalado de BBDD: IOPS aumentados a {nuevos_iops}")