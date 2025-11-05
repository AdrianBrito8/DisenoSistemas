"""
Modulo del servicio concreto ServicioCacheService (Stateless).
"""
from typing import TYPE_CHECKING
from typing_extensions import override

# Imports base
from python_cloud_infra.servicios.aplicaciones.servicio_service import ServicioService

# Imports para inyectar el Strategy (Nuestra lógica fija)
from python_cloud_infra.patrones.strategy.impl.consumo_fijo_strategy import ConsumoFijoStrategy

# Imports para constantes
from python_cloud_infra import constantes as C

# Imports para type hints
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio_cache import ServicioCache


class ServicioCacheService(ServicioService):
    """
    Servicio concreto para la logica de negocio de los Caches (Stateless).
    
    Hereda de ServicioService (la base).
    Inyecta la estrategia de consumo fijo.
    """

    def __init__(self):
        """
        Inicializa el ServicioCacheService.
        
        Aqui se realiza la INYECCION de la estrategia concreta
        (ConsumoFijoStrategy) pasandole la cantidad
        especifica del Cache (2 MW, según US-008).
        
        Referencia: US-008, Rubrica 1.4
        """
        # Inyecta la estrategia constante con el consumo de Cache
        super().__init__(
            ConsumoFijoStrategy(C.CONSUMO_FIJO_CACHE)
        )

    @override
    def mostrar_datos(self, servicio: 'ServicioCache') -> None:
        """
        Muestra los datos especificos de un ServicioCache.
        Implementacion de US-009.

        Args:
            servicio (ServicioCache): La entidad Cache a mostrar.
        """
        # Imprime los datos base
        print(f"Servicio: {servicio.get_tipo()} (Stateless)")
        print(f"Espacio: {servicio.get_espacio_u()} U")
        print(f"Potencia (Fija): {servicio.get_potencia_consumida():.1f} MW")
        print(f"ID: {servicio.get_id()}")
        
        # Imprime los datos especificos de Cache
        print(f"In-Memory: {servicio.is_in_memoria()}")
        print(f"Balanceado: {servicio.is_balanceado()}")