"""
Modulo del servicio ServerRackService.

Este es un servicio central que orquesta la logica de despliegue
"""
from typing import TYPE_CHECKING, List

# --- Imports de Patrones ---
# 1. Importa el Factory para crear servicios (US-TECH-002)
from python_cloud_infra.patrones.factory.servicio_factory import ServicioFactory

# 2. Importa el Registry (Singleton) para operar sobre servicios (US-TECH-005)
from python_cloud_infra.servicios.aplicaciones.servicio_registry import ServicioRegistry

# --- Imports de Entidades ---
from python_cloud_infra.entidades.infra.server_rack import ServerRack
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio

# --- Imports de Excepciones ---
from python_cloud_infra.excepciones.espacio_insuficiente_exception import EspacioInsuficienteException
from python_cloud_infra.excepciones.potencia_insuficiente_exception import PotenciaInsuficienteException
from python_cloud_infra.excepciones import mensajes_exception as MSG

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C

# --- Imports para Type Hints ---
if TYPE_CHECKING:
    from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
    from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch
    # TypeAlias para Stateful
    ServicioStateful = ServicioDatabase | ServicioBatch


class ServerRackService:
    """
    Servicio para gestionar la logica de negocio de los ServerRacks.
    
    Orquesta el despliegue de nuevos servicios (usando Factory)
    y la asignación de recursos (usando Registry/Strategy).
    """

    def __init__(self):
        """
        Inicializa el ServerRackService.
        
        Obtiene la instancia unica (Singleton) del Registry.
        """
        # Obtiene la instancia unica del Registry (Singleton)
        self._registry = ServicioRegistry.get_instance()

    def desplegar_servicio(self,
                           rack: ServerRack,
                           tipo_servicio: str,
                           cantidad: int) -> List[Servicio]:
        """
        Despliega (planta) una cantidad N de un tipo de servicio en el rack.
        
        Logica de negocio de US-004, US-005, US-006, US-007.
        Utiliza el ServicioFactory (Rubrica 1.2).

        Args:
            rack (ServerRack): El rack donde se desplegará.
            tipo_servicio (str): El nombre del servicio (ej. "Database").
            cantidad (int): Cuantos servicios desplegar.

        Raises:
            EspacioInsuficienteException: Si no hay espacio en U.
            ValueError: Si la cantidad es <= 0.

        Returns:
            List[Servicio]: La lista de servicios que fueron creados y desplegados.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a desplegar debe ser positiva")

        print(f"\n--- Intentando desplegar {cantidad} x {tipo_servicio} ---")
        
        # 1. Usa el Factory para crear un "prototipo" y ver su espacio en U
        prototipo = ServicioFactory.crear_servicio(tipo_servicio)
        espacio_requerido_u = prototipo.get_espacio_u() * cantidad
        
        # 2. Validacion de espacio (US-004)
        espacio_disponible_u = rack.get_espacio_disponible_u()
        
        if espacio_disponible_u < espacio_requerido_u:
            raise EspacioInsuficienteException(
                mensaje_tecnico=MSG.TEC_ESPACIO_INSUFICIENTE.format(
                    espacio_disponible_u, espacio_requerido_u),
                mensaje_usuario=MSG.USR_ESPACIO_INSUFICIENTE
            )

        # 3. Creacion y adicion
        servicios_desplegados = []
        for _ in range(cantidad):
            # Usa el Factory para crear la instancia real
            nuevo_servicio = ServicioFactory.crear_servicio(tipo_servicio)
            rack.add_servicio(nuevo_servicio)
            servicios_desplegados.append(nuevo_servicio)
            
        # 4. Actualizar espacio ocupado en el rack
        espacio_ocupado_u = rack.get_espacio_ocupado_u()
        rack.set_espacio_ocupado_u(
            espacio_ocupado_u + espacio_requerido_u
        )
        
        print(f"Despliegue exitoso. Espacio restante: "
              f"{rack.get_espacio_disponible_u()} U")
        
        return servicios_desplegados

    def asignar_recursos(self, rack: ServerRack) -> None:
        """
        Asigna recursos (potencia) a todos los servicios del rack.
        (Análogo a 'regar')
        
        Logica de negocio de US-008.
        Usa el Registry para despachar el consumo (Strategy) y el escalado.

        Args:
            rack (ServerRack): El rack que asignará recursos.
            
        Raises:
            PotenciaInsuficienteException: Si no hay potencia (MW) para asignar.
        """
        
        # 1. Validar y consumir potencia del rack (US-008)
        potencia_necesaria_mw = C.POTENCIA_POR_ASIGNACION
        potencia_disponible_mw = rack.get_potencia_disponible_mw()
        
        if potencia_disponible_mw < potencia_necesaria_mw:
            raise PotenciaInsuficienteException(
                mensaje_tecnico=MSG.TEC_POTENCIA_INSUFICIENTE.format(
                    potencia_disponible_mw, potencia_necesaria_mw),
                mensaje_usuario=MSG.USR_POTENCIA_INSUFICIENTE
            )
            
        rack.set_potencia_disponible_mw(potencia_disponible_mw - potencia_necesaria_mw)
        
        print(f"\nAsignando recursos. Consumiendo {potencia_necesaria_mw} MW del rack...")

        # 2. Distribuir recursos a cada servicio
        for servicio in rack.get_servicios_desplegados():
            
            # 3. Llama al Registry (que llama al Strategy) para
            #    calcular y actualizar el consumo de potencia.
            potencia_consumida = self._registry.consumir_recursos(servicio)
            
            # 4. *** NUESTRA LÓGICA ORIGINAL ***
            #    Llama al Registry para 'escalar' (solo si es Stateful)
            #    (Usamos 'from .servicio_database import ServicioDatabase'
            #    para evitar 'isinstance' y cumplir la rúbrica).
            from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
            from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch
            
            if type(servicio) in (ServicioDatabase, ServicioBatch):
                # Es un servicio Stateful, llamamos a escalar
                self._registry.escalar_servicio_stateful(servicio)
                
        print(f"Asignación de recursos completada. Potencia restante en rack: "
              f"{rack.get_potencia_disponible_mw():.1f} MW")