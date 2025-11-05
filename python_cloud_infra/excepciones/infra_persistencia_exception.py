"""
Modulo de la Excepcion InfraPersistenciaException
"""
from enum import Enum
from .infra_exception import InfraException

class TipoOperacion(Enum):
    """
    Enumera los tipos de operaciones de persistencia.
    (Es idéntico al del proyecto anterior)
    """
    LEER = "Lectura"
    ESCRIBIR = "Escritura"

class InfraPersistenciaException(InfraException):
    """
    Excepcion lanzada cuando ocurre un error durante la
    lectura (deserializacion) o escritura (serializacion) de datos
    del Data Center.
    
    (Es lógicamente idéntica a PersistenciaException)
    
    Referencia: US-021, US-022
    """
    def __init__(self,
                 mensaje_tecnico: str,
                 mensaje_usuario: str,
                 nombre_archivo: str,
                 tipo_operacion: TipoOperacion):
        """
        Inicializa la excepcion de persistencia.

        Args:
            mensaje_tecnico (str): Mensaje tecnico (ej. IOError, PickleError).
            mensaje_usuario (str): Mensaje amigable (ej. "No se pudo leer").
            nombre_archivo (str): El path/nombre del archivo que fallo.
            tipo_operacion (TipoOperacion): Enum LEER o ESCRIBIR.
        """
        super().__init__(mensaje_tecnico, mensaje_usuario)
        self._nombre_archivo = nombre_archivo
        self._tipo_operacion = tipo_operacion

    def get_nombre_archivo(self) -> str:
        """Obtiene el nombre del archivo asociado al error."""
        return self._nombre_archivo

    def get_tipo_operacion(self) -> TipoOperacion:
        """Obtiene el tipo de operacion (Lectura/Escritura) que fallo."""
        return self._tipo_operacion