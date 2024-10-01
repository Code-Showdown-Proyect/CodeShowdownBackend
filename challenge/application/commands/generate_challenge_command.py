from pydantic import BaseModel


class GenerateChallengeCommand(BaseModel):
    difficulty: str
    topic: str
    competition_id: int
