from abc import ABC, abstractmethod
from typing import List, Optional
from competition.domain.entities.competition import Competition
from competition.infrastructure.persistence.models import ChallengeModel


class CompetitionRepository(ABC):

    @abstractmethod
    def create(self, competition: Competition) -> None:
        pass

    @abstractmethod
    def find_by_id(self, competition_id: int) -> Optional[Competition]:
        pass

    @abstractmethod
    def find_by_access_code(self, access_code: str) -> Optional[Competition]:
        pass

    @abstractmethod
    def list_all(self) -> List[Competition]:
        pass

    @abstractmethod
    def update(self, competition: Competition) -> None:
        pass

    @abstractmethod
    def delete(self, competition_id: int) -> None:
        pass
    @abstractmethod
    def get_challenges_by_competition_id(self, competition_id)->List[ChallengeModel]:
        pass