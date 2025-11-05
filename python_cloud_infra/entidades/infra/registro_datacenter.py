"""
Modulo de la entidad RegistroDataCenter.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

# Imports para type hints, evitando importaciones circulares
if TYPE_CHECKING:
    from python_cloud_infra.entidades.infra.datacenter import DataCenter
    from python_cloud_infra.entidades.infra.server_rack import ServerRack

class RegistroDataCenter:
    """
    Entidad que representa el registro oficial completo del DataCenter.

    Agrupa el DataCenter, el ServerRack, el Cliente Corporativo y la Valoración.
    Esta es la entidad principal que se persiste en disco.

    Referencia: US-003
    """

    def __init__(self,
                 id_datacenter: int,
                 datacenter: 'DataCenter',
                 server_rack: 'ServerRack',
                 cliente_corporativo: str,
                 valoracion_activos: float):
        """
        Inicializa el Registro de DataCenter.

        Args:
            id_datacenter (int): ID de DataCenter (debe coincidir con el de DataCenter).
            datacenter (DataCenter): La entidad DataCenter.
            server_rack (ServerRack): La entidad ServerRack.
            cliente_corporativo (str): Nombre del cliente propietario.
            valoracion_activos (float): Valoración fiscal de los activos.

        Raises:
            ValueError: Si la valoración es <= 0.
        """
        if valoracion_activos <= 0:
            raise ValueError("La valoración de activos debe ser positiva")
        
        self._id_datacenter: int = id_datacenter
        self._datacenter: 'DataCenter' = datacenter
        self._server_rack: 'ServerRack' = server_rack
        self._cliente_corporativo: str = cliente_corporativo
        self._valoracion_activos: float = valoracion_activos

    def get_id_datacenter(self) -> int:
        """Obtiene el ID del DataCenter."""
        return self._id_datacenter

    def get_datacenter(self) -> 'DataCenter':
        """Obtiene la entidad DataCenter."""
        return self._datacenter

    def get_server_rack(self) -> 'ServerRack':
        """Obtiene la entidad ServerRack."""
        return self._server_rack

    def get_cliente_corporativo(self) -> str:
        """Obtiene el nombre del cliente corporativo."""
        return self._cliente_corporativo

    def get_valoracion_activos(self) -> float:
        """Obtiene la valoración de activos."""
        return self._valoracion_activos