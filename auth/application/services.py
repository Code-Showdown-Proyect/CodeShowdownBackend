# Lógica de negocio relacionada con la autenticación y registro.
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from auth.domain.entities import User
from auth.domain.value_objects import Email, Password
from auth.domain.repositories import UserRepository
from passlib.context import CryptContext

from auth.infrastructure.security.password_hasher import PasswordHasher

SECRET_KEY = "ccd069ebb51b5d11dfff860e4ee1c7630945a45432771abd58e0f6f1c40968df"
ALGORITHM = "HS256"
Access_token_expire_minutes = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate_user(self, email: Email, password: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if user and self.verify_password(password, user.password):
            return user
        return None

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=Access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def register_user(self, username: str, email: str, password: str) -> User:

        hashed_password = self.get_password_hash(password)

        new_user = User(
            id=None,
            username=username,
            email=email,
            password= hashed_password,
            role="basic",
        )

        self.user_repository.create(new_user)
        return new_user

    def delete_user(self, email: Email) -> bool:
        user = self.user_repository.find_by_email(email)
        if user:
            self.user_repository.delete(user)
            return True
        return False

    def update_username(self, email: Email, new_username: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if user:
            user.username = new_username
            self.user_repository.update(user)
            return user
        return None

    def update_password(self, email: Email, current_password: str, new_password: str) -> bool:
        user = self.user_repository.find_by_email(email)
        if user and PasswordHasher.verify_password(current_password, user.password):
            # Si la contraseña actual es correcta, proceder a actualizarla
            hashed_password = PasswordHasher.hash_password(new_password)
            user.password = hashed_password
            self.user_repository.update(user)
            return True
        return False

