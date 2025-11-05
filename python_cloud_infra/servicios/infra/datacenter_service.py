"""
Modulo del servicio DataCenterService.
"""
from python_cloud_infra.entidades.infra.datacenter import DataCenter
from python_cloud_infra.entidades.infra.server_rack import ServerRack
from python_cloud_infra import constantes as C

class DataCenterService:
    """
    Servicio para gestionar la logica de negocio de los DataCenters.
    """

    def crear_datacenter_con_rack(
        self,
        id_datacenter: int,
        potencia_total_mw: float,
        ubicacion_geografica: str,
        nombre_rack: str,
        espacio_rack_u: int = 42 # Valor default común para un rack
    ) -> DataCenter:
        """
        Crea una entidad DataCenter y su ServerRack asociado,
        y las vincula.
        
        Logica de negocio de US-001 y US-002.

        Args:
            id_datacenter (int): ID unico del DataCenter.
            potencia_total_mw (float): Potencia total del edificio en MW.
            ubicacion_geografica (str): Ubicacion fisica del DC.
            nombre_rack (str): Nombre para el rack principal.
            espacio_rack_u (int, optional): Espacio en U del rack. Defaults a 42.

        Returns:
            DataCenter: La entidad DataCenter creada y ya vinculada.
        """
        
        # 1. Crear el DataCenter (el "edificio")
        datacenter = DataCenter(
            id_datacenter=id_datacenter,
            potencia_total_mw=potencia_total_mw,
            ubicacion_geografica=ubicacion_geografica
        )
        
        # 2. Crear el ServerRack (el "rack" principal)
        rack = ServerRack(
            nombre=nombre_rack,
            espacio_maximo_u=espacio_rack_u,
            datacenter=datacenter,
            potencia=C.POTENCIA_INICIAL_RACK # Usa la constante de US-002
        )
        
        # 3. Vincular el DataCenter con su Rack principal
        # (Esto es clave para que el modelo este completo)
        datacenter.set_rack_principal(rack)
        
        print(f"DataCenter creado (ID {id_datacenter}) "
              f"con ServerRack '{nombre_rack}'.")
        
        return datacenter