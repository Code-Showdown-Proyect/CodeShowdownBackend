from typing import Optional

class JoinCompetitionCommand:
    def __init__(self, access_code: str, password: Optional[str] = None):
        self.access_code = access_code
        self.password = password