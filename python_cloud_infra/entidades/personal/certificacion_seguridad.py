"""
Modulo de la entidad CertificacionSeguridad.
"""
from datetime import date

class CertificacionSeguridad:
    """
    Entidad que representa el certificado de seguridad
    de un SysAdmin.

    Referencia: US-015
    """

    def __init__(self,
                 apto: bool,
                 fecha_emision: date,
                 nivel_certificacion: str,
                 observaciones: str | None = None):
        """
        Inicializa la CertificacionSeguridad.

        Args:
            apto (bool): True si esta apto, False si no.
            fecha_emision (date): Fecha de emision del certificado.
            nivel_certificacion (str): Nivel de la certificacion (ej. "CISSP").
            observaciones (str | None, optional): Observaciones.
        """
        self._apto: bool = apto
        self._fecha_emision: date = fecha_emision
        # --- Atributo Único (Diferenciación) ---
        self._nivel_certificacion: str = nivel_certificacion
        self._observaciones: str | None = observaciones

    def esta_apto(self) -> bool:
        """
        Indica si el SysAdmin esta apto (certificado).

        Returns:
            bool: True si esta apto.
        """
        return self._apto

    def get_fecha_emision(self) -> date:
        """Obtiene la fecha de emision del certificado."""
        return self._fecha_emision
        
    def get_nivel_certificacion(self) -> str:
        """Obtiene el nivel de la certificacion (ej. "CISSP")."""
        return self._nivel_certificacion

    def get_observaciones(self) -> str | None:
        """Obtiene las observaciones, si existen."""
        return self._observaciones