"""
Modulo del servicio CloudProviderService.

Maneja la logica de negocio de alto nivel que
involucra a multiples DataCenters (registros).
"""
from typing import Dict, List, Type, TypeVar, cast

# --- Imports de Entidades y Servicios de Negocio ---
from python_cloud_infra.entidades.infra.registro_datacenter import RegistroDataCenter
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra.servicios.negocio.snapshot import Snapshot

# --- Imports para Type Hints ---
# T es el TypeVar para la cosecha generica
T = TypeVar('T', bound=Servicio)


class CloudProviderService:
    """
    Servicio para gestionar operaciones de alto nivel
    que afectan a multiples DataCenters (Registros).
    
    Implementa US-018, US-019 y US-020.
    """

    def __init__(self):
        """
        Inicializa el CloudProviderService.
        
        Mantiene un diccionario interno de todos los DataCenters
        gestionados, usando el ID de DataCenter como clave.
        
        Referencia: US-018
        """
        self._datacenters_gestionados: Dict[int, RegistroDataCenter] = {}

    def add_datacenter(self, registro: RegistroDataCenter) -> None:
        """
        Agrega un DataCenter (RegistroDataCenter) al servicio
        para que sea gestionado.
        
        Referencia: US-018

        Args:
            registro (RegistroDataCenter): El registro a gestionar.
        """
        id_dc = registro.get_id_datacenter()
        if id_dc not in self._datacenters_gestionados:
            self._datacenters_gestionados[id_dc] = registro
            print(f"DataCenter (ID {id_dc}) agregado al servicio de gestion.")
        else:
            print(f"DataCenter (ID {id_dc}) ya estaba siendo gestionado.")

    def buscar_datacenter(self, id_datacenter: int) -> RegistroDataCenter | None:
        """
        Busca un DataCenter gestionado por su ID.
        
        Referencia: US-018
        
        Args:
            id_datacenter (int): El ID de DataCenter a buscar.

        Returns:
            RegistroDataCenter | None: El registro si se encuentra, o None.
        """
        return self._datacenters_gestionados.get(id_datacenter)

    def aplicar_parche_seguridad(self, id_datacenter: int, nombre_parche: str) -> bool:
        """
        Aplica un parche de seguridad a todos los servicios de un DataCenter.
        (Análogo a 'fumigar')
        
        Implementacion de US-019.

        Args:
            id_datacenter (int): El ID del DataCenter a parchear.
            nombre_parche (str): El nombre del parche (ej. "CVE-2025-1234").

        Returns:
            bool: True si la operacion fue exitosa, False si
                  no se encontro el DataCenter.
        """
        print(f"\n--- Intentando aplicar parche a DataCenter {id_datacenter} ---")
        registro = self.buscar_datacenter(id_datacenter)
        
        if registro is None:
            print(f"Error: DataCenter {id_datacenter} no encontrado.")
            return False
            
        # Logica de parcheo (aqui solo imprimimos)
        rack_nombre = registro.get_server_rack().get_nombre()
        print(f"Aplicando parche '{nombre_parche}' a todos los servicios en "
              f"'{rack_nombre}' (DC {id_datacenter}).")
        return True

    def decomisionar_y_archivar(self, tipo_servicio: Type[T]) -> Snapshot[T]:
        """
        Descomisiona (cosecha) TODOS los servicios de un TIPO especifico de
        TODOS los DataCenters gestionados y los guarda en un Snapshot.
        
        Implementacion de US-020. (Análogo a 'cosechar_yempaquetar')

        Args:
            tipo_servicio (Type[T]): El tipo de servicio a decomisionar
                                     (ej. ServicioWebApp, ServicioDatabase).

        Returns:
            Snapshot[T]: Un snapshot tipo-seguro con los servicios decomisionados.
        """
        print(f"\n--- DECOMISIONANDO todos los {tipo_servicio.__name__} ---")
        
        # 1. Crear el snapshot generico vacio (US-020)
        snapshot_servicios: Snapshot[T] = Snapshot(tipo_servicio)
        
        servicios_decomisionados: List[T] = []

        # 2. Iterar por TODOS los DataCenters gestionados
        for registro in self._datacenters_gestionados.values():
            server_rack = registro.get_server_rack()
            espacio_liberado_u = 0
            
            # 3. Iterar por todos los servicios de ESE rack
            # (Iteramos sobre una copia para poder modificar la original)
            for servicio in server_rack.get_servicios_desplegados(): 
                
                # 4. Comprobar si es del tipo buscado
                if isinstance(servicio, tipo_servicio):
                    # ¡Es del tipo! Lo decomisionamos.
                    # Hacemos 'cast' para ayudar al type checker
                    servicio_decomisionado = cast(T, servicio)
                    
                    servicios_decomisionados.append(servicio_decomisionado)
                    
                    # 5. Removerlo del rack (US-020)
                    server_rack.remove_servicio(servicio_decomisionado)
                    
                    # 6. Contabilizar espacio (U) liberado
                    espacio_liberado_u += servicio_decomisionado.get_espacio_u()

            # 7. Actualizar espacio ocupado del rack
            if espacio_liberado_u > 0:
                espacio_actual_u = server_rack.get_espacio_ocupado_u()
                server_rack.set_espacio_ocupado_u(
                    espacio_actual_u - espacio_liberado_u
                )
                print(f"  Liberadas {espacio_liberado_u} U de espacio en "
                      f"'{server_rack.get_nombre()}'.")

        # 8. Guardar todo en el snapshot
        snapshot_servicios.add_items(servicios_decomisionados)
        
        print(f"DECOMISIÓN TOTAL: {snapshot_servicios.get_cantidad()} "
              f"instancias de {tipo_servicio.__name__}.")
              
        return snapshot_servicios