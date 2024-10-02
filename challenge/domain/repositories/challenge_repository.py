from abc import ABC, abstractmethod
from typing import Optional, List

from challenge.domain.entities.challenge import Challenge


class ChallengeRepository(ABC):

    @abstractmethod
    def find_by_id(self, challenge_id: str) -> Optional[Challenge]:
        """Buscar un reto por su identificador único."""
        pass

    @abstractmethod
    def save(self, challenge_id: str) -> None:
        """Guardar un nuevo reto en la base de datos."""
        pass

    @abstractmethod
    def list_all(self) -> List[Challenge]:
        """Listar todos los retos disponibles."""
        pass

    @abstractmethod
    def delete(self, challenge_id: str) -> bool:
        """Eliminar un reto por su identificador."""
        pass

    @abstractmethod
    def list_all_by_competition_id(self, competition_id: str) -> List[Challenge]:
        """Listar todos los retos de una competencia."""
        pass