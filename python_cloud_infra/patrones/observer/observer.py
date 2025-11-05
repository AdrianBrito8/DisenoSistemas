"""
Modulo de la interfaz abstracta (Observer) Observer.

(Esta implementacion es genérica y reutilizable,
idéntica a la del proyecto PythonForestal).
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# T es un TypeVar, lo que permite la creacion de Generics
# (exigido por Rubrica 1.3 y Rubrica Auto OBSR-003)
T = TypeVar('T')

class Observer(Generic[T], ABC):
    """
    Interfaz (Observer) que define el metodo 'actualizar'.
    Cualquier clase que quiera "observar" a un Observable debe
    implementar esta interfaz.

    Usa Generic[T] para ser tipo-seguro.

    Referencia: US-TECH-003, Rubrica 1.3
    """

    @abstractmethod
    def actualizar(self, evento: T) -> None:
        """
        Metodo llamado por el Observable cuando hay una notificacion.

        Args:
            evento (T): El dato de la notificacion (ej. un float
                        para la carga de CPU, un str, etc.).
        """
        pass