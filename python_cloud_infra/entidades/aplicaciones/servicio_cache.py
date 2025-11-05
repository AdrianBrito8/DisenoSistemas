"""
Modulo de la entidad ServicioCache (Stateless).
"""
from typing_extensions import override
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra import constantes as C

class ServicioCache(Servicio):
    """
    Entidad que representa un servicio de Cache (Stateless).
    
    Hereda de Servicio y añade logica especifica de Caches:
    -   in_memoria (si es un cache en RAM)
    -   balanceado (siempre False)
    
    Referencia: US-007
    """

    def __init__(self, in_memoria: bool):
        """
        Inicializa un ServicioCache.

        Llama al constructor base con los valores de las constantes
        para espacio_u y potencia_base.

        Args:
            in_memoria (bool): True si es un cache In-Memory (ej. Redis).
        """
        # Llama al __init__ de la clase base 'Servicio'
        super().__init__(
            espacio_u=C.ESPACIO_U_CACHE,
            potencia_base=C.POTENCIA_BASE_CACHE
        )
        
        # --- Atributos Únicos (Diferenciación) ---
        self._in_memoria: bool = in_memoria
        
        # US-007 especifica que los Caches son de acceso directo
        self._balanceado: bool = False

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de servicio.

        Returns:
            str: "Cache"
        """
        return "Cache"

    # --- Getters para atributos únicos ---

    def is_in_memoria(self) -> bool:
        """Indica si el cache es In-Memory."""
        return self._in_memoria

    def is_balanceado(self) -> bool:
        """Indica si el servicio esta detras de un balanceador de carga."""
        return self._balanceado