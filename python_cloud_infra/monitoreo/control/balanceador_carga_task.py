"""
Modulo del Controlador de Riego (Thread).
"""
import threading
import time
from typing import TYPE_CHECKING

# --- Imports de Servicios ---
# (Necesitamos el servicio para llamar a 'asignar_recursos')
from python_cloud_infra.servicios.infra.server_rack_service import ServerRackService

# --- Imports de Entidades ---
from python_cloud_infra.entidades.infra.server_rack import ServerRack

# --- Imports de Excepciones ---
from python_cloud_infra.excepciones.potencia_insuficiente_exception import PotenciaInsuficienteException

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C

# --- Imports para Type Hints ---
if TYPE_CHECKING:
    from python_cloud_infra.monitoreo.sensores.sensor_carga_cpu_task import SensorCargaCPUTask
    from python_cloud_infra.monitoreo.sensores.sensor_uso_ram_task import SensorUsoRAMTask


class BalanceadorCargaTask(threading.Thread):
    """
    Controlador de Balanceo de Carga Automatico.
    (Análogo a 'ControlRiegoTask')
    
    1.  Como Thread (US-012): Se ejecuta en un hilo daemon
        separado, evaluando las condiciones de carga
        cada N segundos.
        
    2.  Recibe los sensores y servicios por Inyeccion de
        Dependencias.
        
    3.  Implementa la logica de decision 'OR' (original de este proyecto).
    """
    
    def __init__(self,
                 sensor_cpu: 'SensorCargaCPUTask',
                 sensor_ram: 'SensorUsoRAMTask',
                 rack: ServerRack,
                 rack_service: ServerRackService):
        """
        Inicializa el Controlador.
        
        Configura el thread como 'daemon' (Rubrica 5.1).

        Args:
            sensor_cpu (SensorCargaCPUTask): Instancia del sensor de CPU.
            sensor_ram (SensorUsoRAMTask): Instancia del sensor de RAM.
            rack (ServerRack): El rack sobre el cual actuar.
            rack_service (ServerRackService): El servicio para asignar recursos.
        """
        # 1. Inicializar el Thread
        super().__init__(daemon=True, name="BalanceadorThread")
        
        # 2. Inyeccion de Dependencias
        self._sensor_cpu = sensor_cpu
        self._sensor_ram = sensor_ram
        self._rack = rack
        self._rack_service = rack_service
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
    def _evaluar_condiciones(self) -> bool:
        """
        Evalua si las condiciones para el balanceo se cumplen.
        Logica de negocio de US-012.
        
        Usa el metodo PULL (get_ultima_lectura) de los sensores.
        """
        # 1. Obtener lecturas (PULL)
        cpu = self._sensor_cpu.get_ultima_lectura()
        ram = self._sensor_ram.get_ultima_lectura()
        
        # 2. *** NUESTRA LÓGICA ORIGINAL (OR en lugar de AND) ***
        # Si CUALQUIER sensor supera el umbral, hay que actuar.
        cpu_alta = cpu > C.CPU_MAX_BALANCEO # ej. 80%
        ram_alta = ram > C.RAM_MAX_BALANCEO # ej. 70%
        
        print(f"[{self.name}] Evaluando... "
              f"CPU: {cpu:.1f}% (Alerta: {cpu_alta}), "
              f"RAM: {ram:.1f}% (Alerta: {ram_alta})")
              
        return cpu_alta or ram_alta

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando balanceador de carga automatico...")
        while not self._detenido.is_set():
            
            # 1. Evaluar si hay que asignar recursos
            if self._evaluar_condiciones():
                
                # 2. Intentar asignar recursos
                try:
                    print(f"[{self.name}] ALERTA DE CARGA. Asignando recursos...")
                    self._rack_service.asignar_recursos(self._rack)
                    print(f"[{self.name}] Asignación de recursos finalizada.")
                    
                except PotenciaInsuficienteException as e:
                    # Manejo de excepcion (US-012)
                    print(f"[{self.name}] ERROR DE BALANCEO: {e.get_user_message()}")
                    # No re-lanzamos, solo logueamos y continuamos.
                
            else:
                print(f"[{self.name}] Carga estable. No se asignan recursos.")

            # 3. Esperar
            self._detenido.wait(timeout=C.INTERVALO_CONTROL_BALANCEO)
                
        print(f"[{self.name}] Balanceador de carga detenido.")

    def detener(self) -> None:
        """
        Solicita la detencion del thread de forma segura.
        (US-013)
        """
        print(f"[{self.name}] Solicitando detencion de balanceador...")
        self._detenido.set()