"""
Modulo de la entidad ServicioBatch (Stateful).
"""
from typing_extensions import override
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra.entidades.aplicaciones.tipo_proceso import TipoProceso
from python_cloud_infra import constantes as C

class ServicioBatch(Servicio):
    """
    Entidad que representa un servicio de procesamiento Batch (Stateful).
    
    Hereda de Servicio y añade logica especifica de Batch:
    -   tipo_proceso (ej. ETL, IA)
    -   workers (que será escalable)
    
    Referencia: US-005
    """

    def __init__(self, tipo_proceso: TipoProceso):
        """
        Inicializa un ServicioBatch.

        Llama al constructor base con los valores de las constantes
        para espacio_u y potencia_base.

        Args:
            tipo_proceso (TipoProceso): El enum del tipo de proceso.
        """
        # Llama al __init__ de la clase base 'Servicio'
        super().__init__(
            espacio_u=C.ESPACIO_U_BATCH,
            potencia_base=C.POTENCIA_BASE_BATCH
        )
        
        # --- Atributos Únicos (Diferenciación) ---
        self._tipo_proceso: TipoProceso = tipo_proceso
        
        # Este es el atributo que escalará (análogo a 'altura')
        self._workers: int = C.WORKERS_INICIAL_BATCH

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de servicio.

        Returns:
            str: "Batch"
        """
        return "Batch"

    # --- Getters y Setters para atributos únicos ---

    def get_tipo_proceso(self) -> TipoProceso:
        """Obtiene el tipo de proceso batch."""
        return self._tipo_proceso

    def get_workers(self) -> int:
        """Obtiene la cantidad actual de workers."""
        return self._workers

    def set_workers(self, workers: int) -> None:
        """
        Establece la cantidad actual de workers.
        Sera usado por el servicio de escalado (US-008).

        Args:
            workers (int): Nuevo numero de workers.
        
        Raises:
            ValueError: Si el numero de workers es negativo.
        """
        if workers < 0:
            raise ValueError("El numero de workers no puede ser negativo")
        self._workers = workers