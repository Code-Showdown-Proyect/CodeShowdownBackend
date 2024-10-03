from abc import ABC, abstractmethod
from typing import Optional, List

from feedback.domain.entities.response import Response


class ResponseRepository(ABC):

    @abstractmethod
    def save(self, response: 'Response') -> None:
        """Guarda la respuesta en la base de datos (crea o actualiza)"""
        pass

    @abstractmethod
    def find_by_id(self, participant_id: int) -> list:
        """Encuentra la respuesta por su ID"""
        pass

    @abstractmethod
    def delete(self, response_id: int) -> None:
        """Elimina una respuesta de la base de datos"""
        pass

    @abstractmethod
    def update_response_with_feedback(self, participant_id: int, feedback: str, is_correct: bool)-> None:
        pass
    @abstractmethod
    def update_score(self, participant_id: int, score: list[int])-> None:
        pass