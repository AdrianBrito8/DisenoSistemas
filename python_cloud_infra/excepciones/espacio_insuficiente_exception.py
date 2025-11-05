"""
Modulo de la Excepcion EspacioInsuficienteException
"""
from .infra_exception import InfraException

class EspacioInsuficienteException(InfraException):
    """
    Excepcion lanzada cuando no hay suficiente espacio (en Unidades 'U')
    en un ServerRack para desplegar un nuevo servicio.
    
    Referencia: US-004
    """
    def __init__(self, mensaje_tecnico: str, mensaje_usuario: str):
        """
        Inicializa la excepcion de espacio insuficiente.

        Args:
            mensaje_tecnico (str): Mensaje tecnico detallado.
            mensaje_usuario (str): Mensaje amigable para el usuario.
        """
        super().__init__(mensaje_tecnico, mensaje_usuario)