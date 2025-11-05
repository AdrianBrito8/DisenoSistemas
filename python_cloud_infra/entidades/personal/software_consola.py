"""
Modulo de la entidad SoftwareConsola.
"""

class SoftwareConsola:
    """
    Entidad que representa una herramienta de software (consola)
    que el SysAdmin usa para trabajar.

    Referencia: US-016
    """

    def __init__(self,
                 id_software: int,
                 nombre: str,
                 licencia_activa: bool):
        """
        Inicializa el Software de Consola.

        Args:
            id_software (int): ID unico del software.
            nombre (str): Nombre del software (ej. "SSH Client", "PowerShell").
            licencia_activa (bool): Si el software tiene licencia activa.
        """
        self._id_software: int = id_software
        self._nombre: str = nombre
        self._licencia_activa: bool = licencia_activa

    def get_id_software(self) -> int:
        """Obtiene el ID del software."""
        return self._id_software

    def get_nombre(self) -> str:
        """Obtiene el nombre del software."""
        return self._nombre

    def tiene_licencia_activa(self) -> bool:
        """Indica si el software tiene una licencia activa."""
        return self._licencia_activa