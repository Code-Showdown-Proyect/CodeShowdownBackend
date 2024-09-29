# Definición de la entidad User.

from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    hashed_password: str
    role: str
    created_at: datetime

