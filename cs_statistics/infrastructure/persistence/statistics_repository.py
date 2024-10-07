from typing import Optional

from sqlalchemy.orm import Session
from cs_statistics.domain.entities.statistics import UserStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository
from cs_statistics.infrastructure.persistence.models import UserStatisticsModel
from user_profile.infrastructure.persistence.models import UserProfileModel


class SQLAlchemyStatisticsRepository(StatisticsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_statistics(self, user_id: int) -> Optional[UserStatistics]:
        user_stat = self.session.query(UserStatisticsModel).filter_by(user_id = user_id).first()
        if not user_stat:
            return None
        return self._to_entity(user_stat)


    def save_user_statistics(self, stats: UserStatistics) -> None:
        # Implementación para guardar las estadísticas de competencia
        try:
            user_stats = UserStatisticsModel(
                id=stats.id,
                user_id=stats.user_id,
                competitions_completed=stats.competitions_completed,
                total_score=stats.total_score,
                average_time_per_competition=stats.average_time_per_competition,
                average_score_per_competition=stats.average_score_per_competition,
                average_time_per_challenge=stats.average_time_per_challenge,
                best_score=stats.best_score,
                challenge_completed_count=stats.challenge_completed_count
            )
            self.session.add(user_stats)
            self.session.commit()
            self.session.refresh(user_stats)
            stats.id = user_stats.id
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear la competencia: {e}")

    def get_user_profile(self, user_id: int) -> dict:
        profile = self.session.query(UserProfileModel).filter_by(user_id = user_id).first()
        if profile:
            return {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "description": profile.description,
                "profile_picture_url": profile.profile_picture_url
            }
        return None

    def _to_entity(self, user_stat: UserStatisticsModel) -> UserStatistics:
        return UserStatistics(
            id=None,
            user_id=user_stat.user_id,
            competitions_completed=user_stat.competitions_completed,
            total_score=user_stat.total_score,
            average_time_per_competition=user_stat.average_time_per_competition,
            average_score_per_competition=user_stat.average_score_per_competition,
            average_time_per_challenge=user_stat.average_time_per_challenge,
            best_score=user_stat.best_score,
            challenge_completed_count=user_stat.challenge_completed_count
        )

    def update_user_statistics(self, user_stats: UserStatistics) -> None:
        # Implementación para actualizar las estadísticas de competencia
        try:
            self.session.query(UserStatisticsModel).filter_by(user_id=user_stats.user_id).update({
                "competitions_completed": user_stats.competitions_completed,
                "total_score": user_stats.total_score,
                "average_time_per_competition": user_stats.average_time_per_competition,
                "average_score_per_competition": user_stats.average_score_per_competition,
                "average_time_per_challenge": user_stats.average_time_per_challenge,
                "best_score": user_stats.best_score,
                "challenge_completed_count": user_stats.challenge_completed_count
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar las estadísticas de competencia: {e}")

