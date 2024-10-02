class ResponseAnalysis:
    def __init__(self, is_correct: bool, improvements: str):
        self.is_correct = is_correct #Indica si la respuesta es correcta
        self.improvements = improvements #Sugerencias para mejorar la respuesta

    def __repr__(self):
        return f"ResponseAnalysis(is_correct={self.is_correct}, improvements={self.improvements})"