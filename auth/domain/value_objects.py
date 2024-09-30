# Definición de Value Objects como Email y Password.

from typing import Optional
import re

class Email:
    def __init__(self, value: str):
        if not self.validate_email(value):
            raise ValueError(f"Invalid email format: {value}")
        self.value = value

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def __str__(self):
        return self.value

class Password:
    def __init__(self, value: str):
        if not self.validate_password(value):
            raise ValueError("Password does not meet complexity requirements.")
        self.value = value

    @staticmethod
    def validate_password(password: str) -> bool:
        # Example: Password must be at least 8 characters long with at least one number and one special character.
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        return re.match(pattern, password) is not None

    def __str__(self):
        return '*' * len(self.value)