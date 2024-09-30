from uuid import uuid4


class ChallengeID:
    def __init__(self, id: str = None):
        self.id = id if id else str(uuid4())

    def __eq__(self, other):
        if not isinstance(other, ChallengeID):
            return False
        return self.id == other.id

    def __str__(self):
        return self.id
