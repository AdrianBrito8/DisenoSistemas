"""
Modulo del servicio RegistroDataCenterService.

Maneja la logica de persistencia (guardar/leer) y
la visualizacion de datos completos del registro.
"""

# --- Imports Standard Library ---
import os
import pickle
from typing import TYPE_CHECKING

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C

# --- Imports de Patrones ---
# 1. Importa el Registry (Singleton) para mostrar datos de servicios (US-009)
from python_cloud_infra.servicios.aplicaciones.servicio_registry import ServicioRegistry

# --- Imports de Excepciones ---
from python_cloud_infra.excepciones.infra_persistencia_exception import InfraPersistenciaException, TipoOperacion
from python_cloud_infra.excepciones import mensajes_exception as MSG

# --- Imports de Entidades ---
if TYPE_CHECKING:
    from python_cloud_infra.entidades.infra.registro_datacenter import RegistroDataCenter


class RegistroDataCenterService:
    """
    Servicio para gestionar la logica de negocio de los Registros de DataCenter.
    
    Implementa US-021 (Persistir), US-022 (Leer) y US-023 (Mostrar).
    """

    def __init__(self):
        """
        Inicializa el RegistroDataCenterService.
        
        Obtiene la instancia unica (Singleton) del Registry.
        """
        self._registry = ServicioRegistry.get_instance()

    def mostrar_datos(self, registro: 'RegistroDataCenter') -> None:
        """
        Muestra un reporte completo del registro del DataCenter.
        Implementacion de US-023.
        
        Usa el Registry para despachar polimorficamente
        la visualizacion de cada servicio (US-009).

        Args:
            registro (RegistroDataCenter): El registro a mostrar.
        """
        server_rack = registro.get_server_rack()
        datacenter = registro.get_datacenter()
        servicios = server_rack.get_servicios_desplegados()

        print("\n=================================")
        print("    REGISTRO DATACENTER    ")
        print("=================================")
        print(f"ID DataCenter: {registro.get_id_datacenter()}")
        print(f"Cliente:       {registro.get_cliente_corporativo()}")
        print(f"Valoración:    ${registro.get_valoracion_activos():,.2f}")
        print(f"Ubicación:     {datacenter.get_ubicacion_geografica()}")
        print(f"Espacio Rack:  {server_rack.get_espacio_maximo_u()} U")
        print(f"Desplegados:   {len(servicios)} servicios")
        print("____________________________")
        print("Listado de Servicios desplegados:")
        
        if not servicios:
            print("(No hay servicios desplegados en el rack)")
        else:
            for servicio in servicios:
                print("---")
                # Llama al Registry (Singleton) para que el
                # servicio correcto (DatabaseService, etc.) muestre los datos.
                self._registry.mostrar_datos(servicio)
        
        print("=================================\n")

    def persistir(self, registro: 'RegistroDataCenter') -> str:
        """
        Guarda (serializa) un RegistroDataCenter en disco usando Pickle.
        Implementacion de US-021.

        Args:
            registro (RegistroDataCenter): El objeto a persistir.

        Raises:
            InfraPersistenciaException: Si ocurre un error de IO o Pickle.
            ValueError: Si el nombre del cliente es nulo o vacio.

        Returns:
            str: El path completo del archivo guardado.
        """
        # Usamos el cliente para el nombre de archivo (US-021)
        cliente = registro.get_cliente_corporativo()
        if not cliente:
            raise ValueError("El cliente corporativo no puede ser nulo o vacio")

        # 1. Asegurar que el directorio 'data/' exista
        directorio = C.DIRECTORIO_DATA
        os.makedirs(directorio, exist_ok=True)

        # 2. Construir el path del archivo
        # Reemplazamos espacios por guiones bajos para un nombre de archivo seguro
        nombre_archivo_seguro = cliente.replace(" ", "_").replace(".", "")
        nombre_archivo = f"{nombre_archivo_seguro}{C.EXTENSION_DATA}"
        path_completo = os.path.join(directorio, nombre_archivo)
        
        print(f"\n--- Intentando persistir registro en {path_completo} ---")

        # 3. Escribir el archivo
        try:
            with open(path_completo, 'wb') as f:
                pickle.dump(registro, f)
                
            print(f"Registro de '{cliente}' persistido exitosamente.")
            return path_completo
            
        except (IOError, OSError) as e:
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_IO.format(directorio) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_IO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )
        except pickle.PickleError as e:
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_PICKLE.format(cliente) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_PICKLE,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )
        except Exception as e:
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_ESCRIBIR_OTRO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_ESCRIBIR_OTRO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.ESCRIBIR
            )

    @staticmethod
    def leer_registro(cliente_corporativo: str) -> 'RegistroDataCenter':
        """
        Carga (deserializa) un RegistroDataCenter desde disco.
        Implementacion de US-022.
        
        Es un metodo estatico porque no necesita estado (self).

        Args:
            cliente_corporativo (str): El nombre del cliente (usado para el nombre del archivo).

        Raises:
            InfraPersistenciaException: Si el archivo no existe o esta corrupto.
            ValueError: Si el nombre del cliente es nulo o vacio.

        Returns:
            RegistroDataCenter: El objeto recuperado.
        """
        if not cliente_corporativo:
            raise ValueError("El nombre del cliente no puede ser nulo o vacio")

        # 1. Construir el path del archivo (replicando la logica de 'persistir')
        nombre_archivo_seguro = cliente_corporativo.replace(" ", "_").replace(".", "")
        nombre_archivo = f"{nombre_archivo_seguro}{C.EXTENSION_DATA}"
        path_completo = os.path.join(C.DIRECTORIO_DATA, nombre_archivo)
        
        print(f"\n--- Intentando leer registro desde {path_completo} ---")

        # 2. Validar que el archivo exista
        if not os.path.exists(path_completo):
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_NO_EXISTE.format(path_completo),
                mensaje_usuario=MSG.USR_LEER_NO_EXISTE,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )

        # 3. Leer el archivo
        try:
            with open(path_completo, 'rb') as f:
                registro_leido = pickle.load(f)
                
            print(f"Registro de '{cliente_corporativo}' recuperado exitosamente.")
            return registro_leido
            
        except (pickle.UnpicklingError, EOFError, ImportError, IndexError) as e:
            # Errores comunes de un archivo pickle corrupto o vacio
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_CORRUPTO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_LEER_CORRUPTO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )
        except Exception as e:
            raise InfraPersistenciaException(
                mensaje_tecnico=MSG.TEC_LEER_OTRO.format(path_completo) + f" | Error: {e}",
                mensaje_usuario=MSG.USR_LEER_OTRO,
                nombre_archivo=path_completo,
                tipo_operacion=TipoOperacion.LEER
            )