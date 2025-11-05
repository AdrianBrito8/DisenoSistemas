"""
Modulo del servicio concreto ServicioWebAppService (Stateless).
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
    from python_cloud_infra.entidades.aplicaciones.servicio_webapp import ServicioWebApp


class ServicioWebAppService(ServicioService):
    """
    Servicio concreto para la logica de negocio de las WebApps (Stateless).
    
    Hereda de ServicioService (la base).
    Inyecta la estrategia de consumo fijo.
    """

    def __init__(self):
        """
        Inicializa el ServicioWebAppService.
        
        Aqui se realiza la INYECCION de la estrategia concreta
        (ConsumoFijoStrategy) pasandole la cantidad
        especifica de la WebApp (1 MW).
        
        Referencia: US-008, Rubrica 1.4
        """
        # Inyecta la estrategia constante con el consumo de WebApp
        super().__init__(
            ConsumoFijoStrategy(C.CONSUMO_FIJO_WEBAPP)
        )

    @override
    def mostrar_datos(self, servicio: 'ServicioWebApp') -> None:
        """
        Muestra los datos especificos de una ServicioWebApp.
        Implementacion de US-009.

        Args:
            servicio (ServicioWebApp): La entidad WebApp a mostrar.
        """
        # Imprime los datos base
        print(f"Servicio: {servicio.get_tipo()} (Stateless)")
        print(f"Espacio: {servicio.get_espacio_u()} U")
        print(f"Potencia (Fija): {servicio.get_potencia_consumida():.1f} MW")
        print(f"ID: {servicio.get_id()}")
        
        # Imprime los datos especificos de WebApp
        print(f"Framework: {servicio.get_framework()}")
        print(f"Balanceado: {servicio.is_balanceado()}")