"""
Modulo de la entidad ServicioWebApp (Stateless).
"""
from typing_extensions import override
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra import constantes as C

class ServicioWebApp(Servicio):
    """
    Entidad que representa un servicio de Web App (Stateless).
    
    Hereda de Servicio y añade logica especifica de WebApps:
    -   framework (ej. Flask, Django)
    -   balanceado (siempre True)
    
    Referencia: US-006
    """

    def __init__(self, framework: str):
        """
        Inicializa un ServicioWebApp.

        Llama al constructor base con los valores de las constantes
        para espacio_u y potencia_base.

        Args:
            framework (str): El framework de la app (ej. "Django", "Flask").
        """
        # Llama al __init__ de la clase base 'Servicio'
        super().__init__(
            espacio_u=C.ESPACIO_U_WEBAPP,
            potencia_base=C.POTENCIA_BASE_WEBAPP
        )
        
        # --- Atributos Únicos (Diferenciación) ---
        self._framework: str = framework
        
        # US-006 especifica que las WebApps siempre estan balanceadas
        self._balanceado: bool = True

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de servicio.

        Returns:
            str: "WebApp"
        """
        return "WebApp"

    # --- Getters para atributos únicos ---

    def get_framework(self) -> str:
        """Obtiene el framework de la WebApp."""
        return self._framework

    def is_balanceado(self) -> bool:
        """Indica si el servicio esta detras de un balanceador de carga."""
        return self._balanceado