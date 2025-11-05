"""
Modulo de la clase base (Observable) Observable.

(Esta implementacion es genérica y reutilizable,
idéntica a la del proyecto PythonForestal).
"""
from abc import ABC
from typing import Generic, List
# Importamos el T (TypeVar) desde nuestro modulo observer
from .observer import Observer, T

class Observable(Generic[T], ABC):
    """
    Clase base (Observable) que gestiona una lista de Observers.
    Provee metodos para agregar, eliminar y notificar observadores.

    Usa Generic[T] para ser tipo-seguro.

    Referencia: US-TECH-003, Rubrica 1.3
    """

    def __init__(self):
        """
        Inicializa el Observable con una lista vacia de observadores.
        """
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, observador: Observer[T]) -> None:
        """
        Agrega un observador a la lista.

        Args:
            observador (Observer[T]): El observador a agregar.
        """
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        """
        Elimina un observador de la lista.

        Args:
            observador (Observer[T]): El observador a eliminar.
        """
        try:
            self._observadores.remove(observador)
        except ValueError:
            # No hacer nada si el observador no estaba en la lista
            pass

    def notificar_observadores(self, evento: T) -> None:
        """
        Notifica a TODOS los observadores de la lista,
        pasandoles el evento.

        Args:
            evento (T): El dato de la notificacion a enviar.
        """
        for observador in self._observadores:
            observador.actualizar(evento)