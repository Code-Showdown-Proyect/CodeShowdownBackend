from typing import Optional

class JoinCompetitionCommand:
    def __init__(self, access_code: str, user_id: int , password: Optional[str] = None):
        self.access_code = access_code
        self.password = password
        self.user_id =user_id