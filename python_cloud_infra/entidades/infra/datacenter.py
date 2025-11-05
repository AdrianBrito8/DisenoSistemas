"""
Modulo de la entidad DataCenter.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

# Se usa TYPE_CHECKING para evitar importaciones circulares
# en tiempo de ejecucion con ServerRack.
if TYPE_CHECKING:
    from python_cloud_infra.entidades.infra.server_rack import ServerRack

class DataCenter:
    """
    Entidad que representa un DataCenter físico.

    Contiene informacion sobre su ID, potencia total y ubicación.
    Esta vinculada a uno (y solo uno) ServerRack principal en esta simulación.

    Referencia: US-001
    """

    def __init__(self,
                 id_datacenter: int,
                 potencia_total_mw: float,
                 ubicacion_geografica: str):
        """
        Inicializa el DataCenter.

        Args:
            id_datacenter (int): Numero unico de ID del DataCenter.
            potencia_total_mw (float): Potencia máxima total en MW.
            ubicacion_geografica (str): Ubicacion fisica (ej. "Ashburn, Virginia").

        Raises:
            ValueError: Si el ID es <= 0 o la potencia es <= 0.
        """
        if id_datacenter <= 0:
            raise ValueError("El ID de DataCenter debe ser un numero positivo")
        if potencia_total_mw <= 0:
            raise ValueError("La potencia total debe ser mayor a cero")

        self._id_datacenter: int = id_datacenter
        self._potencia_total_mw: float = potencia_total_mw
        self._ubicacion_geografica: str = ubicacion_geografica
        self._rack_principal: ServerRack | None = None # Se asigna post-creacion

    def get_id_datacenter(self) -> int:
        """Obtiene el ID del DataCenter."""
        return self._id_datacenter

    def get_potencia_total_mw(self) -> float:
        """Obtiene la potencia total del DataCenter en MW."""
        return self._potencia_total_mw

    def set_potencia_total_mw(self, potencia_mw: float) -> None:
        """
        Establece la potencia total del DataCenter.
        Criterio de aceptacion de US-001.

        Args:
            potencia_mw (float): Nueva potencia total en MW.

        Raises:
            ValueError: Si la potencia es <= 0.
        """
        if potencia_mw <= 0:
            raise ValueError("La potencia total debe ser mayor a cero")
        self._potencia_total_mw = potencia_mw

    def get_ubicacion_geografica(self) -> str:
        """Obtiene la ubicación geográfica del DataCenter."""
        return self._ubicacion_geografica

    def get_rack_principal(self) -> ServerRack | None:
        """Obtiene el rack principal asociado a este DataCenter."""
        return self._rack_principal

    def set_rack_principal(self, rack: ServerRack) -> None:
        """
        Asigna el rack principal a este DataCenter.
        
        Args:
            rack (ServerRack): La instancia del ServerRack.
        """
        self._rack_principal = rack