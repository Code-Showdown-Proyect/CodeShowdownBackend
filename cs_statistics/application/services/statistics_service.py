from cs_statistics.domain.entities.statistics import UserStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository


class StatisticsService:
    def __init__(self, statistics_repository: StatisticsRepository):
        self.statistics_repository = statistics_repository

    def get_user_statistics(self, user_id: int)-> dict:
        profile_data = self.statistics_repository.get_user_profile(user_id)
        competition_stats = self.statistics_repository.get_user_statistics(user_id)
        # Aquí se agregaría lógica para agregar datos y formatear el resultado
        formatted_stats = {
            "user_id": user_id,
            "profile": {
                "first_name": profile_data["first_name"],
                "last_name": profile_data["last_name"],
                "description": profile_data["description"],
                "profile_picture_url": profile_data["profile_picture_url"]
            },
            "user_statistics": {
                "total_completed": competition_stats.competitions_completed if competition_stats else 0,
                "total_score": competition_stats.total_score if competition_stats else 0,
                "average_score": competition_stats.average_score_per_competition if competition_stats else 0.0,
                "average_time_per_competition": competition_stats.average_time_per_competition if competition_stats else 0.0,
                "average_time_per_challenge": competition_stats.average_time_per_challenge if competition_stats else 0.0,
                "best_score": competition_stats.best_score if competition_stats else 0,
                "challenge_completed_count": competition_stats.challenge_completed_count if competition_stats else 0
            }
        }
        return formatted_stats

    def update_user_statistics(self, user_id: int, competitions_completed: int = None, total_score: int = None,
                               average_time_per_competition: float = None, average_score_per_competition: float = None, average_time_per_challenge: float = None,
                               best_score: int = None, challenge_completed_count: int = None):
        # Actualizar estadísticas de competencias
        if competitions_completed is not None or total_score is not None or average_time_per_competition is not None or average_score_per_competition is not None:
            user_stats = self.statistics_repository.get_user_statistics(user_id)
            if not user_stats:
                raise ValueError(f"User with id {user_id} does not have any statistics")
            if competitions_completed is not None:
                user_stats.total_completed = competitions_completed
            if total_score is not None:
                user_stats.total_score = total_score
            if average_time_per_competition is not None:
                user_stats.average_time_per_competition = average_time_per_competition
            if average_score_per_competition is not None:
                user_stats.average_score = average_score_per_competition
            if best_score is not None:
                user_stats.best_score = best_score
            if challenge_completed_count is not None:
                user_stats.challenge_completed_count = challenge_completed_count
            if average_time_per_challenge is not None:
                user_stats.average_time_per_challenge = average_time_per_challenge
            self.statistics_repository.update_user_statistics(user_stats)

    def create_user_statistics(self, user_id: int, competitions_completed: int = None, total_score: int = None,
                               average_time_per_competition: float = None, average_score_per_competition: float = None, average_time_per_challenge: float = None,
                               best_score: int = None, challenge_completed_count: int = None)-> UserStatistics:
        # Crear estadísticas de usuario
        user_stats = self.statistics_repository.get_user_statistics(user_id)
        if user_stats:
            raise ValueError(f"User with id {user_id} already has statistics")
        user_stats = UserStatistics(
            id=None,
            user_id=user_id,
            competitions_completed=competitions_completed if competitions_completed else 0,
            total_score=total_score if total_score else 0,
            average_time_per_competition=average_time_per_competition if average_time_per_competition else 0.0,
            average_score_per_competition=average_score_per_competition if average_score_per_competition else 0.0,
            average_time_per_challenge=average_time_per_challenge if average_time_per_challenge else 0.0,
            best_score=best_score if best_score else 0,
            challenge_completed_count=challenge_completed_count if challenge_completed_count else 0
        )
        self.statistics_repository.save_user_statistics(user_stats)
        return user_stats