class UpdateStatusCommand:
    def __init__(self, competition_id: int, status: str):
        self.competition_id = competition_id
        self.status = status