from abc import ABC, abstractmethod
from typing import List, Optional
from competition.domain.entities.participant import Participant


class ParticipantRepository(ABC):

    @abstractmethod
    def create(self, participant: Participant) -> None:
        pass

    @abstractmethod
    def find_by_id(self, participant_id: int) -> Optional[Participant]:
        pass

    @abstractmethod
    def list_by_competition(self, competition_id: int) -> List[Participant]:
        pass

    @abstractmethod
    def update(self, participant: Participant) -> None:
        pass

    @abstractmethod
    def delete(self, participant_id: int) -> None:
        pass

    @abstractmethod
    def find_by_competition_id(self, competition_id: int)->list:
        pass

    @abstractmethod
    def find_by_user_and_competition(self, user_id: int, competition_id: int) -> Participant:
        pass
