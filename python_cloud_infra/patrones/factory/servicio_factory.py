"""
Modulo de la implementacion del Patron Factory Method.
"""
from typing_extensions import override

# Imports de Entidades (las 4 clases que crea esta factory)
from python_cloud_infra.entidades.aplicaciones.servicio import Servicio
from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
from python_cloud_infra.entidades.aplicaciones.servicio_batch import ServicioBatch
from python_cloud_infra.entidades.aplicaciones.servicio_webapp import ServicioWebApp
from python_cloud_infra.entidades.aplicaciones.servicio_cache import ServicioCache

# Imports de Enums (valores por defecto)
from python_cloud_infra.entidades.aplicaciones.tipo_proceso import TipoProceso


class ServicioFactory:
    """
    Implementa el patron Factory Method para la creacion de Servicios.

    Centraliza la logica de instanciacion, desacoplando al cliente
    (ej. ServerRackService) de las clases concretas.

    Referencia: US-TECH-002, Rubrica 1.2, Rubrica Auto FACT-*
    """

    @staticmethod
    def _crear_database() -> Servicio:
        """Metodo factory privado para crear ServicioDatabase."""
        # US-004: Valores por defecto
        return ServicioDatabase(motor="PostgreSQL", version="16.1")

    @staticmethod
    def _crear_batch() -> Servicio:
        """Metodo factory privado para crear ServicioBatch."""
        # US-005: Valores por defecto
        return ServicioBatch(tipo_proceso=TipoProceso.ETL)

    @staticmethod
    def _crear_webapp() -> Servicio:
        """Metodo factory privado para crear ServicioWebApp."""
        # US-006: Valores por defecto
        return ServicioWebApp(framework="Flask")

    @staticmethod
    def _crear_cache() -> Servicio:
        """Metodo factory privado para crear ServicioCache."""
        # US-007: Valores por defecto
        return ServicioCache(in_memoria=True)

    @staticmethod
    def crear_servicio(tipo_servicio: str) -> Servicio:
        """
        Metodo factory principal y publico.

        Utiliza un diccionario para el dispatch, cumpliendo con
        Rubrica 1.2 y Rubrica Auto (FACT-004).

        Args:
            tipo_servicio (str): El tipo de servicio a crear (ej. "Database").

        Raises:
            ValueError: Si el tipo de servicio es desconocido.

        Returns:
            Servicio: Una instancia de una subclase de Servicio.
        """
        # El diccionario de factories exigido por la rubrica.
        # NO USAR LAMBDAS (Rubrica 3.4)
        factories = {
            "Database": ServicioFactory._crear_database,
            "Batch": ServicioFactory._crear_batch,
            "WebApp": ServicioFactory._crear_webapp,
            "Cache": ServicioFactory._crear_cache
        }

        if tipo_servicio not in factories:
            raise ValueError(f"Tipo de servicio desconocido: {tipo_servicio}")

        # Llama al metodo factory privado correspondiente
        creador_servicio = factories[tipo_servicio]
        servicio_creado = creador_servicio()
        
        return servicio_creado