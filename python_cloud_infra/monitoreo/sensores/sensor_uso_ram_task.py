"""
Modulo del Sensor de Uso de RAM (Thread y Observable).
"""
import threading
import time
import random
from typing_extensions import override

# --- Imports de Patrones ---
from python_cloud_infra.patrones.observer.observable import Observable

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C

class SensorUsoRAMTask(threading.Thread, Observable[float]):
    """
    Sensor de Uso de RAM.
    
    1.  Como Thread (US-011): Se ejecuta en un hilo daemon separado
        leyendo el uso de RAM cada N segundos.
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
        threading.Thread.__init__(self, daemon=True, name="SensorRAMThread")
        
        # 2. Inicializar el Observable EXPLICITAMENTE
        Observable.__init__(self)
        
        # 3. Control de detencion (Graceful Shutdown - US-013)
        self._detenido: threading.Event = threading.Event()
        
        # 4. Almacenamiento de ultima lectura (para PULL del Balanceador)
        self._ultima_lectura: float = 40.0 # Un valor inicial default (RAM media)

    def _leer_uso_ram(self) -> float:
        """Simula la lectura de un sensor de RAM."""
        ram = random.uniform(C.SENSOR_RAM_MIN, C.SENSOR_RAM_MAX)
        return ram

    def run(self) -> None:
        """
        Metodo principal del Thread.
        Se ejecuta al llamar a .start()
        """
        print(f"[{self.name}] Iniciando sensor de uso de RAM...")
        while not self._detenido.is_set():
            # 1. Leer valor
            carga_ram = self._leer_uso_ram()
            
            # 2. Guardar valor (para PULL)
            self._ultima_lectura = carga_ram
            
            # 3. Notificar (PUSH - Observer Pattern)
            # (Rubrica 1.3)
            self.notificar_observadores(carga_ram)
            
            # 4. Esperar
            self._detenido.wait(timeout=C.INTERVALO_SENSOR_RAM)
                
        print(f"[{self.name}] Sensor de uso de RAM detenido.")

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
            float: El ultimo uso de RAM registrado (%).
        """
        return self._ultima_lectura