"""
Modulo de la entidad generica Snapshot.
(Análoga a 'Paquete[T]')
"""
from typing import Generic, List, TypeVar, Type

# T es un TypeVar, lo que permite la creacion de Generics
# (exigido por Rubrica 3.3 y US-020)
T = TypeVar('T')

class Snapshot(Generic[T]):
    """
    Entidad generica que representa un snapshot (archivo) de
    servicios decomisionados.
    
    Usa Generic[T] para ser tipo-seguro (ej. Snapshot[ServicioDatabase],
    Snapshot[ServicioWebApp]).
    
    Referencia: US-020
    """
    _contador_id: int = 0

    def __init__(self, tipo_contenido: Type[T]):
        """
        Inicializa un snapshot vacio.

        Args:
            tipo_contenido (Type[T]): El tipo de servicio que
                                      contendra este snapshot.
        """
        Snapshot._contador_id += 1
        self._id_snapshot: int = Snapshot._contador_id
        self._tipo_contenido: Type[T] = tipo_contenido
        self._contenido: List[T] = []

    def get_id_snapshot(self) -> int:
        """Obtiene el ID unico del snapshot."""
        return self._id_snapshot

    def get_tipo_contenido(self) -> Type[T]:
        """Obtiene el TIPO de contenido (ej. <class 'ServicioWebApp'>)."""
        return self._tipo_contenido
    
    def get_nombre_tipo_contenido(self) -> str:
        """Obtiene el nombre legible del tipo (ej. 'ServicioWebApp')."""
        return self._tipo_contenido.__name__

    def get_contenido(self) -> List[T]:
        """Obtiene la lista de servicios dentro del snapshot."""
        return self._contenido.copy()

    def add_item(self, item: T) -> None:
        """Añade un servicio al snapshot."""
        self._contenido.append(item)
        
    def add_items(self, items: List[T]) -> None:
        """Añade una lista de servicios al snapshot."""
        self._contenido.extend(items)

    def get_cantidad(self) -> int:
        """Obtiene la cantidad de servicios en el snapshot."""
        return len(self._contenido)

    def mostrar_contenido_snapshot(self) -> None:
        """
        Imprime un resumen del contenido del snapshot.
        Implementacion de US-020.
        """
        print("\nContenido del Snapshot:")
        print(f"  Tipo: {self.get_nombre_tipo_contenido()}")
        print(f"  Cantidad: {self.get_cantidad()}")
        print(f"  ID Snapshot: {self.get_id_snapshot()}")