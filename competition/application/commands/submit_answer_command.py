class SubmitAnswerCommand:
    def __init__(self, participant_id: int, competition_id: int, answer: str, exercise_id=None, time_taken=None):
        self.participant_id = participant_id
        self.competition_id = competition_id
        self.answer = answer
        self.exercise_id = exercise_id
        self.time_taken = time_taken
