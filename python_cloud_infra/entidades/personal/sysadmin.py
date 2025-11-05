"""
Modulo de la entidad SysAdmin.
"""
from __future__ import annotations
from typing import List, TYPE_CHECKING

# Imports para type hints
from python_cloud_infra.entidades.personal.ticket_soporte import TicketSoporte
if TYPE_CHECKING:
    from python_cloud_infra.entidades.personal.certificacion_seguridad import CertificacionSeguridad

class SysAdmin:
    """
    Entidad que representa a un Administrador de Sistemas (SysAdmin).

    Contiene sus datos personales, la lista de tickets asignados
    y su certificado de seguridad.

    Referencia: US-014
    """

    def __init__(self,
                 id_empleado: int,
                 nombre: str,
                 tickets: List[TicketSoporte]):
        """
        Inicializa el SysAdmin.

        Args:
            id_empleado (int): ID unico del empleado.
            nombre (str): Nombre completo.
            tickets (List[TicketSoporte]): Lista de tickets de soporte asignados.
        
        Raises:
            ValueError: Si el ID de empleado es <= 0.
        """
        if id_empleado <= 0:
            raise ValueError("El ID de empleado debe ser un numero positivo")
            
        self._id_empleado: int = id_empleado
        self._nombre: str = nombre
        
        # Guardamos una copia para cumplir con US-014 (inmutabilidad)
        # y Rubrica 5.2 (Defensive Copying)
        self._tickets: List[TicketSoporte] = tickets.copy()
        
        # US-014: Inicia sin certificacion
        self._certificacion: 'CertificacionSeguridad' | None = None

    def get_id_empleado(self) -> int:
        """Obtiene el ID de empleado del SysAdmin."""
        return self._id_empleado

    def get_nombre(self) -> str:
        """Obtiene el nombre completo del SysAdmin."""
        return self._nombre

    def get_tickets(self) -> List[TicketSoporte]:
        """
        Obtiene una COPIA de la lista de tickets.
        (US-014, Rubrica 5.2: Defensive Copying)

        Returns:
            List[TicketSoporte]: Una copia de la lista de tickets.
        """
        return self._tickets.copy()

    def get_certificacion(self) -> 'CertificacionSeguridad' | None:
        """
        Obtiene la certificacion de seguridad del SysAdmin, si existe.

        Returns:
            CertificacionSeguridad | None: La certificacion, o None si no tiene.
        """
        return self._certificacion

    def set_certificacion(self, certificacion: 'CertificacionSeguridad') -> None:
        """
        Asigna o actualiza la certificacion de seguridad.
        (Necesario para US-015)

        Args:
            certificacion (CertificacionSeguridad): El nuevo certificado.
        """
        self._certificacion = certificacion