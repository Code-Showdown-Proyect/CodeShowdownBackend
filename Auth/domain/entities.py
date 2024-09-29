# Definición de la entidad User.

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime


@dataclass
class User:
    id: int
    username: str
    email: str
    password: str
    role: str
    created_at: datetime = field(default_factory=datetime.utcnow)

