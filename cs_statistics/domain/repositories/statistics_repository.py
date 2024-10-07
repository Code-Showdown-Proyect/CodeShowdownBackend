from abc import ABC, abstractmethod
from typing import Optional

from cs_statistics.domain.entities.statistics import UserStatistics


class StatisticsRepository(ABC):

    @abstractmethod
    def get_user_statistics(self, user_id: int) -> Optional[UserStatistics]:
        """Obtiene las estadísticas de competencia para un usuario dado."""
        pass

    @abstractmethod
    def save_user_statistics(self, stats: UserStatistics) -> UserStatistics:
        """Obtiene las estadísticas de competencia para un usuario dado."""
        pass
    @abstractmethod
    def get_user_profile(self, user_id: int)-> dict:
        """Obtiene los datos de un usuario."""
        pass
    @abstractmethod
    def update_user_statistics(self, stats: UserStatistics) -> None:
        """Actualiza las estadísticas de competencia para un usuario."""
        pass