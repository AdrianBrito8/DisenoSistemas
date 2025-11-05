"""
Modulo del Sensor de Carga de CPU (Thread y Observable).
"""
import threading
import time
import random
from typing_extensions import override

# --- Imports de Patrones ---
from python_cloud_infra.patrones.observer.observable import Observable

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C

class SensorCargaCPUTask(threading.Thread, Observable[float]):
    """
    Sensor de Carga de CPU.
    
    1.  Como Thread (US-010): Se ejecuta en un hilo daemon separado
        leyendo la carga de CPU cada N segundos.
    2.  Como Observable[float] (US-TECH-003): Notifica a sus
        observadores cada vez que tiene una nueva lectura.
    """
    
    def __init__(self):
        """
        Inicializa el sensor.
        
        Configura el thread como 'daemon' (Rubrica 5.1) y aplica la
        corrección de herencia múltiple (llamadas explícitas a __init__).
        """
        # 1. Inicializar el Thread EXPLICITAMENTE
        threading.Thread.__init__(self, daemon=True, name="SensorCPUThread")
        
        # 2. Inicializar el Observable EXPLICITAMENTE
        Observable.__init__(self)
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
        # 4. Almacenamiento de ultima lectura (para PULL del Balanceador)
        self._ultima_lectura: float = 20.0 # Un valor inicial default (CPU baja)

    def _leer_carga_cpu(self) -> float:
        """Simula la lectura de un sensor de CPU."""
        carga = random.uniform(C.SENSOR_CPU_MIN, C.SENSOR_CPU_MAX)
        return carga

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando sensor de carga de CPU...")
        while not self._detenido.is_set():
            # 1. Leer valor
            carga_cpu = self._leer_carga_cpu()
            
            # 2. Guardar valor (para PULL)
            self._ultima_lectura = carga_cpu
            
            # 3. Notificar (PUSH - Observer Pattern)
            # (Rubrica 1.3)
            self.notificar_observadores(carga_cpu)
            
            # 4. Esperar
            # Usa 'wait' en lugar de 'sleep' para detencion instantanea
            self._detenido.wait(timeout=C.INTERVALO_SENSOR_CPU)
                
        print(f"[{self.name}] Sensor de carga de CPU detenido.")

    def detener(self) -> None:
        """
        Solicita la detencion del thread de forma segura.
        (US-013)
        """
        print(f"[{self.name}] Solicitando detencion de sensor...")
        self._detenido.set()

    def get_ultima_lectura(self) -> float:
        """
        Permite al sistema (BalanceadorCargaTask) obtener
        la ultima lectura (metodo PULL).
        
        Returns:
            float: La ultima carga de CPU registrada (%).
        """
        return self._ultima_lectura