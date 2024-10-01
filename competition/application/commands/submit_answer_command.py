class SubmitAnswerCommand:
    def __init__(self, participant_id: int, competition_id: int, answer: str):
        self.participant_id = participant_id
        self.competition_id = competition_id
        self.answer = answer