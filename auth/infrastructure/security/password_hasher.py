# Lógica para cifrar y verificar contraseñas.
from passlib.context import CryptContext

# Contexto para hashing de contraseñas utilizando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Toma una contraseña en texto plano y devuelve una versión cifrada.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Toma una contraseña en texto plano y una contraseña cifrada,
        y verifica si coinciden.
        """
        return pwd_context.verify(plain_password, hashed_password)