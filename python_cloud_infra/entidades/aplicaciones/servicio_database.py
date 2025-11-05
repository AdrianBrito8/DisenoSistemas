"""
Modulo de la entidad ServicioDatabase (Stateful).
"""
from typing_extensions import override
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra import constantes as C

class ServicioDatabase(Servicio):
    """
    Entidad que representa un servicio de Base de Datos (Stateful).
    
    Hereda de Servicio y añade logica especifica de BBDD:
    -   motor (ej. PostgreSQL)
    -   version
    -   iops (que será escalable)
    
    Referencia: US-004
    """

    def __init__(self, motor: str, version: str):
        """
        Inicializa un ServicioDatabase.

        Llama al constructor base con los valores de las constantes
        para espacio_u y potencia_base.

        Args:
            motor (str): El motor de la BBDD (ej. "PostgreSQL", "MySQL").
            version (str): La version del motor (ej. "15.3").
        """
        # Llama al __init__ de la clase base 'Servicio'
        super().__init__(
            espacio_u=C.ESPACIO_U_DATABASE,
            potencia_base=C.POTENCIA_BASE_DATABASE
        )
        
        # --- Atributos Únicos (Diferenciación) ---
        # Estos atributos no existen en el proyecto 'Pino'.
        self._motor: str = motor
        self._version: str = version
        
        # Este es el atributo que escalará (análogo a 'altura')
        self._iops: int = C.IOPS_INICIAL_DATABASE

    @override
    def get_tipo(self) -> str:
        """
        Obtiene el tipo de servicio.

        Returns:
            str: "Database"
        """
        return "Database"

    # --- Getters y Setters para atributos únicos ---

    def get_motor(self) -> str:
        """Obtiene el motor de la BBDD."""
        return self._motor

    def get_version(self) -> str:
        """Obtiene la version del motor."""
        return self._version

    def get_iops(self) -> int:
        """Obtiene los IOPS (Input/Output Operations Per Second) actuales."""
        return self._iops

    def set_iops(self, iops: int) -> None:
        """
        Establece los IOPS actuales.
        Sera usado por el servicio de escalado (US-008).

        Args:
            iops (int): Nuevo valor de IOPS.
        
        Raises:
            ValueError: Si los IOPS son negativos.
        """
        if iops < 0:
            raise ValueError("Los IOPS no pueden ser negativos")
        self._iops = iops