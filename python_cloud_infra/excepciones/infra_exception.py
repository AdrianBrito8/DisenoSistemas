"""
Modulo de la Excepcion base InfraException (análoga a ForestacionException)
"""

class InfraException(Exception):
    """
    Clase base para todas las excepciones personalizadas del sistema (Dominio CloudInfra).
    Referencia: Rubrica 2.3
    """
    def __init__(self, mensaje_tecnico: str, mensaje_usuario: str):
        """
        Inicializa la excepcion.

        Args:
            mensaje_tecnico (str): El mensaje detallado para el desarrollador.
            mensaje_usuario (str): El mensaje simple para el usuario final.
        """
        super().__init__(mensaje_tecnico)
        self._mensaje_tecnico = mensaje_tecnico
        self._mensaje_usuario = mensaje_usuario

    def get_mensaje_tecnico(self) -> str:
        """Obtiene el mensaje tecnico."""
        return self._mensaje_tecnico

    def get_user_message(self) -> str:
        """Obtiene el mensaje amigable para el usuario."""
        return self._mensaje_usuario