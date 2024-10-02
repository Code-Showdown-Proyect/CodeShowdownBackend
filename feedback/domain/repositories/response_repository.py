from abc import ABC, abstractmethod
from typing import Optional

from feedback.domain.entities.response import Response


class ResponseRepository(ABC):

    @abstractmethod
    def save(self, response: 'Response') -> None:
        """Guarda la respuesta en la base de datos (crea o actualiza)"""
        pass

    @abstractmethod
    def find_by_id(self, response_id: int) -> Optional['Response']:
        """Encuentra la respuesta por su ID"""
        pass

    @abstractmethod
    def delete(self, response_id: int) -> None:
        """Elimina una respuesta de la base de datos"""
        pass