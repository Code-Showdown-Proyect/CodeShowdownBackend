class DeleteCompetitionCommand:
    def __init__(self, competition_id: int, creator_id: int):
        self.competition_id = competition_id
        self.creator_id = creator_id