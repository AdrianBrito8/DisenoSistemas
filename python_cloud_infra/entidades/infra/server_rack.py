"""
Modulo de la entidad ServerRack (Contenedor).
(Análoga a 'Plantacion')
"""
from __future__ import annotations
from typing import List, TYPE_CHECKING

# Imports para type hints, evitando importaciones circulares
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
    from python_cloud_infra.entidades.personal.sysadmin import SysAdmin
    from python_cloud_infra.entidades.infra.datacenter import DataCenter

# Importamos la constante que definimos
from python_cloud_infra import constantes as C

class ServerRack:
    """
    Entidad que representa el rack de servidores (el contenedor).

    Contiene la logica de gestion de espacio (U), potencia (MW),
    y las listas de servicios desplegados y personal asignado.

    Referencia: US-002
    """

    def __init__(self,
                 nombre: str,
                 espacio_maximo_u: int,
                 datacenter: 'DataCenter',
                 potencia: float = C.POTENCIA_INICIAL_RACK):
        """
        Inicializa el ServerRack.

        Args:
            nombre (str): Nombre identificatorio (ej. "Rack A-01").
            espacio_maximo_u (int): Espacio total en Unidades de Rack (ej. 42).
            datacenter (DataCenter): El DataCenter al que esta asociado.
            potencia (float, optional): Potencia disponible en MW. 
                                        Defaults a POTENCIA_INICIAL_RACK (100 MW).
        """
        self._nombre: str = nombre
        self._espacio_maximo_u: int = espacio_maximo_u
        self._espacio_ocupado_u: int = 0
        self._potencia_disponible_mw: float = potencia
        self._datacenter: 'DataCenter' = datacenter
        
        self._servicios_desplegados: List['Servicio'] = []
        self._sysadmins_asignados: List['SysAdmin'] = []

    def get_nombre(self) -> str:
        """Obtiene el nombre del rack."""
        return self._nombre

    def get_espacio_maximo_u(self) -> int:
        """Obtiene el espacio maximo en Unidades de Rack (U)."""
        return self._espacio_maximo_u

    def get_espacio_ocupado_u(self) -> int:
        """Obtiene el espacio en U actualmente ocupado por servicios."""
        return self._espacio_ocupado_u

    def set_espacio_ocupado_u(self, espacio_u: int) -> None:
        """
        Establece el espacio ocupado en U.
        
        Args:
            espacio_u (int): Nuevo espacio ocupado.

        Raises:
            ValueError: Si el espacio es < 0 o > espacio maximo.
        """
        if espacio_u < 0:
            raise ValueError("El espacio ocupado no puede ser negativo")
        if espacio_u > self._espacio_maximo_u:
            raise ValueError("El espacio ocupado no puede superar el maximo")
        self._espacio_ocupado_u = espacio_u
        
    def get_espacio_disponible_u(self) -> int:
        """
        Calcula y obtiene el espacio en U aun disponible.

        Returns:
            int: Espacio disponible en U.
        """
        return self._espacio_maximo_u - self._espacio_ocupado_u

    def get_potencia_disponible_mw(self) -> float:
        """Obtiene la potencia (MW) disponible en el rack."""
        return self._potencia_disponible_mw

    def set_potencia_disponible_mw(self, potencia_mw: float) -> None:
        """
        Establece la potencia disponible.
        Criterio de aceptacion de US-002.

        Args:
            potencia_mw (float): Nueva cantidad de potencia en MW.

        Raises:
            ValueError: Si la potencia es negativa.
        """
        if potencia_mw < 0:
            raise ValueError("La potencia (MW) no puede ser negativa")
        self._potencia_disponible_mw = potencia_mw
        
    def get_datacenter(self) -> 'DataCenter':
        """Obtiene la entidad DataCenter asociada."""
        return self._datacenter

    # --- Gestion de Listas (con Copias Defensivas - Rubrica 5.2) ---

    def get_servicios_desplegados(self) -> List['Servicio']:
        """
        Obtiene una COPIA de la lista de servicios desplegados.
        (Análoga a get_cultivos(), Rubrica 5.2: Defensive Copying)

        Returns:
            List[Servicio]: Una copia de la lista de servicios.
        """
        return self._servicios_desplegados.copy()

    def add_servicio(self, servicio: 'Servicio') -> None:
        """Añade un servicio al rack."""
        self._servicios_desplegados.append(servicio)

    def remove_servicio(self, servicio: 'Servicio') -> None:
        """
        Remueve un servicio del rack.
        (Necesario para US-020: Descomisionar)
        """
        if servicio in self._servicios_desplegados:
            self._servicios_desplegados.remove(servicio)

    def get_sysadmins_asignados(self) -> List['SysAdmin']:
        """
        Obtiene una COPIA de la lista de SysAdmins.
        (Análoga a get_trabajadores(), US-017, Rubrica 5.2)

        Returns:
            List[SysAdmin]: Una copia de la lista de SysAdmins.
        """
        return self._sysadmins_asignados.copy()

    def set_sysadmins_asignados(self, sysadmins: List['SysAdmin']) -> None:
        """
        Establece la lista de SysAdmins, guardando una COPIA.
        (Análoga a set_trabajadores(), US-017, Rubrica 5.2)
        
        Args:
            sysadmins (List[SysAdmin]): La nueva lista de SysAdmins.
        """
        self._sysadmins_asignados = sysadmins.copy()