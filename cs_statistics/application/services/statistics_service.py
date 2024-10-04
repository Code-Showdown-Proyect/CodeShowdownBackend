from cs_statistics.domain.entities.statistics import ParticipantPerformanceStatistics, FeedbackImprovementStatistics, \
    CompetitionStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository
from cs_statistics.infrastructure.external.feedback_client import FeedbackClient
from cs_statistics.infrastructure.external.profile_client import ProfileClient


class StatisticsService:
    def __init__(self, statistics_repository: StatisticsRepository, profile_client: ProfileClient,
                 feedback_client: FeedbackClient):
        self.statistics_repository = statistics_repository
        self.profile_client = profile_client
        self.feedback_client = feedback_client

    def get_user_statistics(self, user_id: int):
        profile_data = self.profile_client.get_user_profile(user_id)
        competition_stats = self.statistics_repository.get_competition_statistics(user_id)
        performance_stats = self.statistics_repository.get_challenge_statistics(user_id)
        feedback_stats = self.statistics_repository.get_feedback_statistics(user_id)

        # Aquí se agregaría lógica para agregar datos y formatear el resultado
        formatted_stats = {
            "user_id": user_id,
            "profile": {
                "first_name": profile_data.get("first_name"),
                "last_name": profile_data.get("last_name"),
                "description": profile_data.get("description"),
                "profile_picture_url": profile_data.get("profile_picture_url")
            },
            "competition_statistics": {
                "total_completed": competition_stats.competitions_completed if competition_stats else 0,
                "total_score": competition_stats.total_score if competition_stats else 0,
                "average_score": competition_stats.average_score if competition_stats else 0.0,
                "average_time_per_question": competition_stats.average_time_per_question if competition_stats else 0.0,
                "average_time_per_competition": competition_stats.average_time_per_competition if competition_stats else 0.0
            },
            "performance_statistics": {
                "average_result": performance_stats.average_score if performance_stats else 0.0,
                "best_score": performance_stats.best_score if performance_stats else 0,
                "average_time_per_challenge": performance_stats.average_resolution_time if performance_stats else 0.0
            },
            "feedback_statistics": {
                "suggestions_applied": feedback_stats.suggestions_applied if feedback_stats else 0
            }
        }

        return formatted_stats

    def update_user_statistics(self, user_id: int, competitions_completed: int = None, total_score: int = None,
                               average_time_per_competition: float = None, average_score_per_competition: float = None,
                               challenges_completed: int = None, best_score: int = None,
                               average_time_per_challenge: float = None, feedback_applied_count: int = None):
        # Actualizar estadísticas de competencias
        if competitions_completed is not None or total_score is not None or average_time_per_competition is not None or average_score_per_competition is not None:
            competition_stats = self.statistics_repository.get_competition_statistics(user_id)
            if not competition_stats:
                competition_stats = CompetitionStatistics(user_id, 0, 0.0, 0, 0.0, 0.0)
            if competitions_completed is not None:
                competition_stats.total_completed = competitions_completed
            if total_score is not None:
                competition_stats.total_score = total_score
            if average_time_per_competition is not None:
                competition_stats.average_time_per_competition = average_time_per_competition
            if average_score_per_competition is not None:
                competition_stats.average_score = average_score_per_competition
            self.statistics_repository.save_competition_statistics(competition_stats)

        # Actualizar estadísticas de desafíos
        if challenges_completed is not None or best_score is not None or average_time_per_challenge is not None:
            performance_stats = self.statistics_repository.get_challenge_statistics(user_id)
            if not performance_stats:
                performance_stats = ParticipantPerformanceStatistics(user_id, 0.0, 0, 0.0)
            if challenges_completed is not None:
                performance_stats.average_result = challenges_completed  # Aquí se actualizaría de acuerdo a los datos reales
            if best_score is not None:
                performance_stats.best_score = best_score
            if average_time_per_challenge is not None:
                performance_stats.average_time_per_challenge = average_time_per_challenge
            self.statistics_repository.save_challenge_statistics(performance_stats)

        # Actualizar estadísticas de retroalimentación
        if feedback_applied_count is not None:
            feedback_stats = self.statistics_repository.get_feedback_statistics(user_id)
            if not feedback_stats:
                feedback_stats = FeedbackImprovementStatistics(user_id, 0)
            feedback_stats.suggestions_applied = feedback_applied_count
            self.statistics_repository.save_feedback_statistics(feedback_stats)