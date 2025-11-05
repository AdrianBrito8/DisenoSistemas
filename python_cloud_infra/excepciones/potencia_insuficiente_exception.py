"""
Modulo de la Excepcion PotenciaInsuficienteException
"""
from .infra_exception import InfraException

class PotenciaInsuficienteException(InfraException):
    """
    Excepcion lanzada cuando no hay suficiente potencia (en MW)
    en un ServerRack para realizar una operacion (ej. asignar_recursos).
    
    Referencia: US-008
    """
    def __init__(self, mensaje_tecnico: str, mensaje_usuario: str):
        """
        Inicializa la excepcion de potencia insuficiente.

        Args:
            mensaje_tecnico (str): Mensaje tecnico detallado.
            mensaje_usuario (str): Mensaje amigable para el usuario.
        """
        super().__init__(mensaje_tecnico, mensaje_usuario)