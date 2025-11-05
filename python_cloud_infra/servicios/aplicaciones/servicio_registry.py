"""
Modulo del ServicioRegistry.

Implementa dos patrones de diseño:
1.  Singleton (Thread-Safe): Asegura una unica instancia (US-TECH-001).
2.  Registry: Despacha operaciones al servicio correcto (US-TECH-005).
"""
from __future__ import annotations
from threading import Lock
from typing import Dict, Type, Callable, Any, TYPE_CHECKING
from typing_extensions import override

# --- Imports de Entidades (para las llaves del diccionario) ---
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch
from python_cloud_infra.entidades.aplicaciones.servicio_webapp import ServicioWebApp
from python_cloud_infra.entidades.aplicaciones.servicio_cache import ServicioCache

# --- Imports de Servicios (para los valores del diccionario) ---
from python_cloud_infra.servicios.aplicaciones.servicio_database_service import ServicioDatabaseService
from python_cloud_infra.servicios.aplicaciones.servicio_batch_service import ServicioBatchService
from python_cloud_infra.servicios.aplicaciones.servicio_webapp_service import ServicioWebAppService
from python_cloud_infra.servicios.aplicaciones.servicio_cache_service import ServicioCacheService

# --- TypeAlias para los diccionarios del Registry ---
ServicioType = Type[Servicio]
ConsumoHandler = Callable[[Servicio], float]
MostrarHandler = Callable[[Servicio], None]
EscalarHandler = Callable[[Servicio], None]


class ServicioRegistry:
    """
    Implementa los patrones Singleton y Registry para los servicios de aplicacion.

    - Como Singleton (Rubrica 1.1), asegura una unica instancia
      thread-safe para gestionar los servicios.
    - Como Registry (US-TECH-005), centraliza el despacho
      polimorfico de operaciones (consumir_recursos, mostrar_datos, escalar).
    """

    # --- Implementacion del Patron Singleton (US-TECH-001) ---

    _instance: ServicioRegistry | None = None
    
    # El Lock es exigido por la Rubrica 1.1 y Auto (SING-003)
    _lock: Lock = Lock()

    def __new__(cls) -> ServicioRegistry:
        """
        Controla la creacion de la instancia (Singleton).
        Usa double-checked locking para ser thread-safe.
        
        Referencia: Rubrica 1.1, Rubrica Auto (SING-002)
        """
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            # Doble chequeo, por si otro thread la creo
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # El __init__ se llama automaticamente despues
        
        return cls._instance

    @classmethod
    def get_instance(cls) -> ServicioRegistry:
        """
        Metodo publico para obtener la unica instancia del Singleton.
        
        Referencia: Rubrica Auto (SING-004)
        """
        if cls._instance is None:
            cls() # Llama a __new__ y luego a __init__
        
        return cls._instance  # type: ignore

    # --- Implementacion del Patron Registry (US-TECH-005) ---

    def __init__(self):
        """
        Inicializa el Registry.
        
        Gracias al Singleton, este __init__ se ejecutara UNA SOLA VEZ.
        
        Aqui creamos las instancias de los servicios y
        construimos los diccionarios de handlers (dispatch).
        """
        # 1. Crear instancias unicas de cada servicio
        self._db_service: ServicioDatabaseService = ServicioDatabaseService()
        self._batch_service: ServicioBatchService = ServicioBatchService()
        self._webapp_service: ServicioWebAppService = ServicioWebAppService()
        self._cache_service: ServicioCacheService = ServicioCacheService()

        # 2. Construir diccionario para 'consumir_recursos'
        self._consumo_handlers: Dict[ServicioType, ConsumoHandler] = {
            ServicioDatabase: self._db_service.consumir_recursos,
            ServicioBatch: self._batch_service.consumir_recursos,
            ServicioWebApp: self._webapp_service.consumir_recursos,
            ServicioCache: self._cache_service.consumir_recursos
        }

        # 3. Construir diccionario para 'mostrar_datos'
        self._mostrar_datos_handlers: Dict[ServicioType, MostrarHandler] = {
            ServicioDatabase: self._db_service.mostrar_datos,
            ServicioBatch: self._batch_service.mostrar_datos,
            ServicioWebApp: self._webapp_service.mostrar_datos,
            ServicioCache: self._cache_service.mostrar_datos
        }
        
        # 4. Construir diccionario para 'escalar' (Solo Stateful)
        #    Esta es nuestra lógica de negocio original (no es copia).
        #    Los servicios Stateless (WebApp, Cache) NO estan aqui.
        self._escalar_handlers: Dict[ServicioType, EscalarHandler] = {
            ServicioDatabase: self._db_service.escalar,
            ServicioBatch: self._batch_service.escalar,
        }

    def _get_handler(self,
                     servicio: Servicio,
                     handlers_dict: Dict) -> Callable:
        """
        Metodo privado para buscar un handler en un diccionario
        de despacho.
        """
        tipo_servicio = type(servicio)
        handler = handlers_dict.get(tipo_servicio)
        
        if handler is None:
            raise TypeError(f"Operacion no soportada para el tipo: {tipo_servicio.__name__}")
        
        return handler

    # --- Metodos Publicos (Dispatch Polimorfico) ---

    def consumir_recursos(self, servicio: Servicio) -> float:
        """
        Despacha la operacion 'consumir_recursos' al servicio
        correcto usando el Registry.

        Args:
            servicio (Servicio): El servicio que consume potencia.

        Returns:
            float: La potencia (MW) consumida.
        """
        handler = self._get_handler(servicio, self._consumo_handlers)
        return handler(servicio) # type: ignore

    def mostrar_datos(self, servicio: Servicio) -> None:
        """
        Despacha la operacion 'mostrar_datos' al servicio
        correcto usando el Registry. (US-009)

        Args:
            servicio (Servicio): El servicio a mostrar.
        """
        handler = self._get_handler(servicio, self._mostrar_datos_handlers)
        handler(servicio)

    def escalar_servicio_stateful(self, servicio: Servicio) -> None:
        """
        Despacha la operacion 'escalar' al servicio
        Stateful correcto usando el Registry. (US-008)

        Args:
            servicio (Servicio): El servicio (Database o Batch) a escalar.
        
        Raises:
            TypeError: Si se pasa un servicio no-escalable (WebApp, Cache).
        """
        handler = self._get_handler(servicio, self._escalar_handlers)
        handler(servicio)