# Implementación del UserRepository, que interactúa con la base de datos.
# auth/infrastructure/repositories/user_repository.py
from sqlalchemy.orm import Session
from Auth.domain.repositories import UserRepository
from Auth.domain.entities import User
from Auth.domain.value_objects import Email
from Auth.infrastructure.persistence.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_email(self, email: Email) -> User:
        user_record = self.session.query(UserModel).filter(UserModel.email == email.value).first()
        if user_record:
            return User(
                id=user_record.id,
                username=user_record.username,
                email=user_record.email,
                password=user_record.password,
                role=user_record.role,
                created_at=user_record.created_at
            )
        return None

    def create(self, user: User) -> None:
        user_model = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            role=user.role,
            created_at=user.created_at
        )
        self.session.add(user_model)
        self.session.commit()