from datetime import datetime
from typing import List


class Challenge:
    def __init__(self, id: int, title: str, description: str, difficulty: str, tags: List[str], created_at: datetime, output_example: str):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.tags = tags
        self.created_at = created_at
        self.output_example = output_example

    def __repr__(self):
        return f"Challenge(id={self.id}, title={self.title}, difficulty={self.difficulty}, tags={self.tags}"