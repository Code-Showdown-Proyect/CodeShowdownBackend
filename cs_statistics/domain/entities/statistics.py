class CompetitionStatistics:
    def __init__(self, user_id: int, competitions_completed: int, average_score: float, total_score: int, average_time_per_question: float, average_time_per_competition: float):

        self.user_id = user_id  # ID del usuario
        self.competitions_completed = competitions_completed  # Total de competencias completadas por el usuario
        self.average_score = average_score  # Puntaje promedio por competencia
        self.total_score = total_score  # Puntaje total acumulado
        self.average_time_per_question = average_time_per_question  # Tiempo promedio por pregunta (en segundos)
        self.average_time_per_competition = average_time_per_competition  # Tiempo promedio por competencia (en segundos)

    def __repr__(self):
        return f"CompetitionStatistics(user_id={self.user_id}, competitions_completed={self.competitions_completed}, average_score={self.average_score}, total_score={self.total_score}, average_time_per_question={self.average_time_per_question}, average_time_per_competition={self.average_time_per_competition})"


class ParticipantPerformanceStatistics:
    def __init__(self, user_id: int, average_result: float, best_score: int, average_time_per_challenge: float):
        self.user_id = user_id  # ID del usuario
        self.average_result = average_result  # Resultado promedio obtenido por competencia y desafíos
        self.best_score = best_score  # Mejor puntaje obtenido en competencias
        self.average_time_per_challenge = average_time_per_challenge  # Tiempo promedio tomado para completar desafíos (en segundos)

    def __repr__(self):
        return f"ParticipantPerformanceStatistics(user_id={self.user_id}, average_result={self.average_result}, best_score={self.best_score}, average_time_per_challenge={self.average_time_per_challenge})"


class ChallengeStatistics:
    def __init__(self, challenge_id: int, average_resolution_time: float, best_score: int = None, average_score: float = None):
        self.challenge_id = challenge_id  # ID del desafío
        self.average_resolution_time = average_resolution_time  # Tiempo promedio de resolución del desafío (en segundos)
        self.best_score = best_score  # Mejor puntaje obtenido para este desafío (opcional)
        self.average_score = average_score  # Puntaje promedio obtenido para este desafío (opcional)


    def __repr__(self):
        return f"ChallengeStatistics(challenge_id={self.challenge_id}, average_resolution_time={self.average_resolution_time}, best_score={self.best_score})"


class FeedbackImprovementStatistics:
    def __init__(self, user_id: int, suggestions_applied: int):
        self.user_id = user_id  # ID del usuario
        self.suggestions_applied = suggestions_applied  # Cantidad de sugerencias de mejora aplicadas

    def __repr__(self):
        return f"FeedbackImprovementStatistics(user_id={self.user_id}, suggestions_applied={self.suggestions_applied})"


class UserStatistics:
    def __init__(self, user_id: int, competition_stats: CompetitionStatistics, performance_stats: ParticipantPerformanceStatistics, feedback_stats: FeedbackImprovementStatistics):
        self.user_id = user_id  # ID del usuario
        self.competition_stats = competition_stats  # Estadísticas de competencias del usuario
        self.performance_stats = performance_stats  # Estadísticas de rendimiento del usuario en los desafíos
        self.feedback_stats = feedback_stats  # Estadísticas de mejora de código y retroalimentación

    def __repr__(self):
        return f"UserStatistics(user_id={self.user_id}, competition_stats={self.competition_stats}, performance_stats={self.performance_stats}, feedback_stats={self.feedback_stats})"