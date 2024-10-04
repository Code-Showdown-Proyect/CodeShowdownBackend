from abc import ABC, abstractmethod

from cs_statistics.domain.entities.statistics import CompetitionStatistics, FeedbackImprovementStatistics, \
    ChallengeStatistics


class StatisticsRepository(ABC):

    @abstractmethod
    def get_competition_statistics(self, user_id: int) -> CompetitionStatistics:
        """Obtiene las estadísticas de competencia para un usuario dado."""
        pass

    @abstractmethod
    def get_challenge_statistics(self, user_id: int) -> ChallengeStatistics:
        """Obtiene las estadísticas de desafío para un usuario dado."""
        pass

    @abstractmethod
    def get_feedback_statistics(self, user_id: int) -> FeedbackImprovementStatistics:
        """Obtiene las estadísticas de mejora de retroalimentación para un usuario dado."""
        pass

    @abstractmethod
    def save_competition_statistics(self, stats: CompetitionStatistics) -> None:
        """Guarda las estadísticas de competencia."""
        pass

    @abstractmethod
    def save_challenge_statistics(self, stats: ChallengeStatistics) -> None:
        """Guarda las estadísticas de desafío."""
        pass

    @abstractmethod
    def save_feedback_statistics(self, stats: FeedbackImprovementStatistics) -> None:
        """Guarda las estadísticas de retroalimentación."""
        pass