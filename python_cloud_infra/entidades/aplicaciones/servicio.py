"""
Modulo de la clase base abstracta Servicio.
"""
from abc import ABC, abstractmethod

class Servicio(ABC):
    """
    Clase base abstracta para todos los tipos de servicios de aplicacion.

    Define la interfaz comun que debe tener cualquier servicio desplegado,
    incluyendo el espacio en 'U' que ocupa, la potencia base que consume
    y un ID unico.
    """

    # Variable de clase para autoincrementar el ID
    _contador_id: int = 0

    def __init__(self, espacio_u: int, potencia_base: float):
        """
        Inicializa un nuevo servicio.

        Args:
            espacio_u (int): El espacio en Unidades de Rack (U) que ocupa.
            potencia_base (float): El consumo de potencia base en MW.

        Raises:
            ValueError: Si el espacio es <= 0 o la potencia es < 0.
        """
        if espacio_u <= 0:
            raise ValueError("El espacio en U debe ser mayor a cero")
        if potencia_base < 0:
            raise ValueError("La potencia base no puede ser negativa")
        
        Servicio._contador_id += 1
        self._id: int = Servicio._contador_id
        self._espacio_u: int = espacio_u
        self._potencia_consumida: float = potencia_base

    def get_id(self) -> int:
        """
        Obtiene el ID unico del servicio.

        Returns:
            int: El ID.
        """
        return self._id

    def get_espacio_u(self) -> int:
        """
        Obtiene el espacio en Unidades de Rack (U) que ocupa el servicio.

        Returns:
            int: El espacio en U.
        """
        return self._espacio_u

    def get_potencia_consumida(self) -> float:
        """
        Obtiene la cantidad de potencia (MW) consumida actualmente.

        Returns:
            float: Potencia en MW.
        """
        return self._potencia_consumida

    def set_potencia_consumida(self, potencia: float) -> None:
        """
        Establece la potencia consumida actual del servicio.

        Args:
            potencia (float): Nueva potencia en MW.

        Raises:
            ValueError: Si la potencia es negativa.
        """
        if potencia < 0:
            raise ValueError("La potencia consumida no puede ser negativa")
        self._potencia_consumida = potencia

    @abstractmethod
    def get_tipo(self) -> str:
        """
        Metodo abstracto para obtener el tipo de servicio.
        Debe ser implementado por las clases hijas.

        Returns:
            str: El nombre del tipo de servicio (ej. "Database", "WebApp").
        """
        pass