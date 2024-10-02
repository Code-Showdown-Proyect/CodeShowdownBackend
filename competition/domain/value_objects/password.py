import re

class Password:
    def __init__(self, password: str):
        if not self.is_valid_password(password):
            raise ValueError("Password must be at least 8 characters long and contain both letters and numbers.")
        self.password = password

    def is_valid_password(self, password: str) -> bool:
        """Verifica que la contraseña tenga al menos 8 caracteres y contenga letras y números"""
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))

    def __str__(self) -> str:
        return self.password

    def __eq__(self, other) -> bool:
        return isinstance(other, Password) and self.password == other.password