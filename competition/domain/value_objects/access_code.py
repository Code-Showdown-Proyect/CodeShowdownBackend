import re

class AccessCode:
    def __init__(self, code: str):
        if not self.is_valid_code(code):
            raise ValueError(f"Invalid access code: {code}")
        self.code = code

    def is_valid_code(self, code: str) -> bool:
        """Verifica que el código tenga un formato válido (6 caracteres alfanuméricos)"""
        return bool(re.match(r'^[A-Z0-9]{6}$', code))

    def __str__(self) -> str:
        return self.code

    def __eq__(self, other) -> bool:
        return isinstance(other, AccessCode) and self.code == other.code