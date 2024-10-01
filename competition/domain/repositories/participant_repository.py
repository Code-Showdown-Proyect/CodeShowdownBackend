from abc import ABC, abstractmethod
from typing import List, Optional
from competition.domain.entities.participant import Participant


class ParticipantRepository(ABC):

    @abstractmethod
    def create(self, participant: Participant) -> None:
        """Crea un nuevo participante en el repositorio"""
        pass

    @abstractmethod
    def find_by_id(self, participant_id: int) -> Optional[Participant]:
        """Busca un participante por su ID"""
        pass

    @abstractmethod
    def list_by_competition(self, competition_id: int) -> List[Participant]:
        """Lista todos los participantes de una competencia específica"""
        pass

    @abstractmethod
    def update(self, participant: Participant) -> None:
        """Actualiza la información de un participante"""
        pass

    @abstractmethod
    def delete(self, participant_id: int) -> None:
        """Elimina un participante del repositorio"""
        pass

    @abstractmethod
    def find_by_competition_id(self, competition_id: int)->list:
        pass