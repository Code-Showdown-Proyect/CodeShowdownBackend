class UserStatistics:
    def __init__(self, id: int, user_id: int, competitions_completed: int, total_score: int, average_time_per_competition: float, average_score_per_competition: float, average_time_per_challenge: float, best_score: int, challenge_completed_count: int):
        self.id= id
        self.user_id = user_id  # ID del usuario
        self.competitions_completed = competitions_completed
        self.total_score = total_score
        self.average_time_per_competition = average_time_per_competition
        self.average_score_per_competition = average_score_per_competition
        # Challenge statistics
        self.average_time_per_challenge = average_time_per_challenge
        self.best_score = best_score
        self.challenge_completed_count = challenge_completed_count

    def __repr__(self):
        return f"UserStatistics(user_id={self.user_id}, competitions_completed={self.competitions_completed}, total_score={self.total_score}, average_time_per_competition={self.average_time_per_competition}, average_score_per_competition={self.average_score_per_competition}, average_time_per_challenge={self.average_time_per_challenge}, best_score={self.best_score}, challenge_completed_count={self.challenge_completed_count})"

