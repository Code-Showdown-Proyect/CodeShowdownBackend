class CompletionRate:
    def __init__(self, value: float):
        if value < 0 or value > 100:
            raise ValueError("Completion rate must be between 0 and 100")
        self.value = value

    def __repr__(self):
        return f"CompletionRate(value={self.value})"

class AverageScore:
    def __init__(self, value: float):
        if value < 0:
            raise ValueError("Average score must be non-negative")
        self.value = value

    def __repr__(self):
        return f"AverageScore(value={self.value})"