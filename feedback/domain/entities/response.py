from typing import Optional


class Response:
    def __init__(self, id: int, participant_id: int, challenge_id: int, answer: str, time_taken: str, feedback: Optional['Feedback'] = None):
        self.id = id                          # ID de la respuesta
        self.participant_id = participant_id  # ID del participante que respondió
        self.challenge_id = challenge_id      # ID del desafío al que pertenece la pregunta
        self.answer = answer                  # Respuesta enviada por el participante
        self.time_taken = time_taken          # Tiempo tomado para responder
        self.feedback = feedback              # Retroalimentación generada (puede ser None al principio)

    def __repr__(self):
        return f"Response(id={self.id}, participant_id={self.participant_id}, challenge_id={self.challenge_id}, answer={self.answer})"