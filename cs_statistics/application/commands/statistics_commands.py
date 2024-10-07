from typing import Optional


class UpdateStatisticsCommand:
    def __init__(self, user_id: int, competitions_completed: Optional[int] = None, total_score: Optional[int] = None,
                 average_time_per_competition: Optional[float] = None, average_score_per_competition: Optional[float] = None,
                 average_time_per_challenge: Optional[float] = None, best_score: Optional[int] = None,
                 challenge_completed_count: Optional[int] = None):
        self.user_id = user_id  # ID del usuario
        self.competitions_completed = competitions_completed
        self.total_score = total_score
        self.average_time_per_competition = average_time_per_competition
        self.average_score_per_competition = average_score_per_competition
        # Challenge statistics
        self.average_time_per_challenge = average_time_per_challenge
        self.best_score = best_score
        self.challenge_completed_count = challenge_completed_count

class CreateStatisticsCommand:
    def __init__(self, user_id: int):
        self.user_id = user_id