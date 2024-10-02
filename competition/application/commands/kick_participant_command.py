class KickParticipantCommand:
    def __init__(self, competition_id: int, creator_id: int, participant_id: int):
        self.competition_id = competition_id
        self.creator_id = creator_id
        self.participant_id = participant_id