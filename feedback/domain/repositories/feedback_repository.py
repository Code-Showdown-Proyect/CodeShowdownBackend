from abc import ABC, abstractmethod
from typing import Optional
from feedback.domain.entities.feedback import Feedback

class FeedbackRepository(ABC):

    @abstractmethod
    def save(self, feedback: 'Feedback') -> None:
        """Guarda la retroalimentación en la base de datos"""
        pass

    @abstractmethod
    def find_by_response_id(self, response_id: int) -> Optional['Feedback']:
        """Encuentra la retroalimentación por el ID de la respuesta"""
        pass

    @abstractmethod
    def delete(self, feedback_id: int) -> None:
        """Elimina la retroalimentación de la base de datos"""
        pass