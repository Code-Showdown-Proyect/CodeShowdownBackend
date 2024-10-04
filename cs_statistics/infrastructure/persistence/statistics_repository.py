from sqlalchemy.orm import Session
from cs_statistics.domain.entities.statistics import CompetitionStatistics, ChallengeStatistics, FeedbackImprovementStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository
from cs_statistics.infrastructure.persistence.models import CompetitionStatisticsModel, ChallengeStatisticsModel, FeedbackImprovementStatisticsModel


class SQLAlchemyStatisticsRepository(StatisticsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_competition_statistics(self, user_id: int) -> CompetitionStatistics:
        competition_stat = self.session.query(CompetitionStatisticsModel).filter(CompetitionStatisticsModel.user_id == user_id).first()
        if competition_stat:
            return CompetitionStatistics(
                user_id=competition_stat.user_id,
                competitions_completed=competition_stat.competitions_completed,
                total_score=competition_stat.total_score,
                average_time_per_question=competition_stat.average_time_per_question,
                average_time_per_competition=competition_stat.average_time_per_competition,
                average_score=competition_stat.average_score
            )
        return None

    def get_challenge_statistics(self, challenge_id: int) -> ChallengeStatistics:
        challenge_stat = self.session.query(ChallengeStatisticsModel).filter(ChallengeStatisticsModel.challenge_id == challenge_id).first()
        if challenge_stat:
            return ChallengeStatistics(
                challenge_id=challenge_stat.challenge_id,
                average_resolution_time=challenge_stat.average_resolution_time,
                best_score=challenge_stat.best_score
            )
        return None

    def get_feedback_statistics(self, user_id: int) -> FeedbackImprovementStatistics:
        feedback_stat = self.session.query(FeedbackImprovementStatisticsModel).filter(FeedbackImprovementStatisticsModel.user_id == user_id).first()
        if feedback_stat:
            return FeedbackImprovementStatistics(
                user_id=feedback_stat.user_id,
                suggestions_applied=feedback_stat.suggestions_applied
            )
        return None

    def save_competition_statistics(self, stats: CompetitionStatistics) -> None:
        # Implementación para guardar las estadísticas de competencia
        pass

    def save_challenge_statistics(self, stats: ChallengeStatistics) -> None:
        # Implementación para guardar las estadísticas del desafío
        pass

    def save_feedback_statistics(self, stats: FeedbackImprovementStatistics) -> None:
        # Implementación para guardar las estadísticas de retroalimentación
        pass