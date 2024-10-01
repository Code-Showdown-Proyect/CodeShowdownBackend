class CreateCompetitionCommand:
    def __init__(self, name: str, number_of_exercises: int, time_limit: int, password: str = None):
        self.name = name
        self.number_of_exercises = number_of_exercises
        self.time_limit = time_limit
        self.password = password