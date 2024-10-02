from datetime import datetime
from typing import Optional


class UpdateCompetitionCommand:
    def __init__(self, competition_id: int, name: str, start_date: datetime, number_of_exercises: int, password: Optional[str] = None, creator_id: int = None, time_limit: int = 10):
        self.time_limit = time_limit
        self.competition_id = competition_id
        self.name = name
        self.start_date = start_date
        self.number_of_exercises = number_of_exercises
        self.password = password
        self.creator_id = creator_id

