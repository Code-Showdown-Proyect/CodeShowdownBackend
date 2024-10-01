from datetime import datetime

class CompetitionSession:
    def __init__(self, id: int, competition_id: int, current_exercise: int, start_time: datetime, end_time: datetime = None):
        self.id = id
        self.competition_id = competition_id
        self.current_exercise = current_exercise
        self.start_time = start_time
        self.end_time = end_time

    def end_session(self, end_time: datetime):
        self.end_time = end_time

    def __repr__(self):
        return (f"CompetitionSession(id={self.id}, "
                f"competition_id={self.competition_id}, "
                f"current_exercise={self.current_exercise}, "
                f"start_time={self.start_time}, end_time={self.end_time})")