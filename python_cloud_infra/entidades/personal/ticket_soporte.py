"""
Modulo de la entidad TicketSoporte.
"""
from datetime import date
from enum import Enum

class EstadoTicket(Enum):
    """
    Enumera los estados posibles de un TicketSoporte.
    (Análogo a 'EstadoTarea')
    """
    ABIERTO = "Abierto"
    CERRADO = "Cerrado"

class TicketSoporte:
    """
    Entidad que representa un ticket de soporte asignado a un SysAdmin.

    Referencia: US-014
    """

    def __init__(self,
                 id_ticket: int,
                 fecha: date,
                 descripcion: str):
        """
        Inicializa el TicketSoporte.

        Args:
            id_ticket (int): ID unico del ticket.
            fecha (date): Fecha de apertura del ticket.
            descripcion (str): Descripcion del problema (ej. "Servidor caido").
        """
        self._id_ticket: int = id_ticket
        self._fecha: date = fecha
        self._descripcion: str = descripcion
        # Un ticket siempre inicia como ABIERTO
        self._estado: EstadoTicket = EstadoTicket.ABIERTO 

    def get_id_ticket(self) -> int:
        """Obtiene el ID del ticket."""
        return self._id_ticket

    def get_fecha(self) -> date:
        """Obtiene la fecha de apertura del ticket."""
        return self._fecha

    def get_descripcion(self) -> str:
        """Obtiene la descripcion del ticket."""
        return self._descripcion

    def get_estado(self) -> EstadoTicket:
        """Obtiene el estado actual del ticket (Abierto/Cerrado)."""
        return self._estado

    def cerrar_ticket(self) -> None:
        """
        Marca el ticket como CERRADO.
        (Necesario para US-016)
        """
        self._estado = EstadoTicket.CERRADO