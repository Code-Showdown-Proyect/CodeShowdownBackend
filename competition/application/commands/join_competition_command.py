class JoinCompetitionCommand:
    def __init__(self, access_code: str, password: str = None):
        self.access_code = access_code
        self.password = password