from typing import Optional


class Feedback:
    def __init__(self, response_id: int, is_correct: bool, detail: str, score: int, analyzed_at: Optional[str] = None):
        self.response_id = response_id            # ID de la respuesta a la que pertenece la retroalimentación
        self.is_correct = is_correct              # Indica si la respuesta es correcta
        self.detail = detail                  # Retroalimentación detallada
        self.score = score                        # Puntaje asignado basado en la calidad de la respuesta
        self.analyzed_at = analyzed_at            # Fecha en que se realizó el análisis

    def __repr__(self):
        return (f"Feedback(response_id={self.response_id}, is_correct={self.is_correct}, "
                f"score={self.score}, analyzed_at={self.analyzed_at})")