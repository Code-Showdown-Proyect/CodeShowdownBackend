from datetime import datetime

class Participant:
    def __init__(self, id: int, user_id: int, competition_id: int, score: int = 0, joined_at: datetime = None):
        self.id = id
        self.user_id = user_id  # Referencia al ID de usuario (relacionado con la tabla `Users`)
        self.competition_id = competition_id
        self.score = score
        self.joined_at = joined_at if joined_at else datetime.utcnow()

    def add_score(self, points: int):
        self.score += points

    def __repr__(self):
        return (f"Participant(id={self.id}, "
                f"user_id={self.user_id}, "
                f"competition_id={self.competition_id}, "
                f"score={self.score})")