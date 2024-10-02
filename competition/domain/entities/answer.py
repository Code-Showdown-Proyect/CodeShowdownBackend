
class Answer:
    def __init__(self, id: int, participant_id: int, challenge_id: int, answer: str, time_taken: int):
        self.id = id
        self.participant_id = participant_id
        self.challenge_id = challenge_id
        self.answer = answer
        self.time_taken = time_taken



    def __repr__(self):
        return f"Answer(id={self.id}, participant_id={self.participant_id}, exercise_id={self.exercise_id})"