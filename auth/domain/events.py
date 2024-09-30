# Definición de los eventos de dominio (e.g., UserRegistered).

from dataclasses import dataclass
from datetime import datetime
from pydantic import tools


@dataclass
class UserRegistered:
    user_id: int
    email: str
    timestamp: datetime


tools.display_dataframe_to_user(name="auth Domain Folder Structure", dataframe=None)