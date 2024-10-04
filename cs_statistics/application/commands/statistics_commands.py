from typing import Optional


class UpdateStatisticsCommand:
    def __init__(self, user_id: int, competitions_completed: Optional[int] = None, total_score: Optional[int] = None,
                 average_time_per_question: Optional[float] = None, average_time_per_competition: Optional[float] = None):
        self.user_id = user_id
        self.competitions_completed= competitions_completed
        self.total_score = total_score
        self.average_time_per_question = average_time_per_question
        self.average_time_per_competition = average_time_per_competition

class CreateStatisticsCommand:
    def __init__(self, user_id: int):
        self.user_id = user_id