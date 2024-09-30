# Implementación del UserRepository, que interactúa con la base de datos.
# auth/infrastructure/repositories/user_repository.py
from sqlalchemy.orm import Session
from auth.domain.repositories import UserRepository
from auth.domain.entities import User
from auth.domain.value_objects import Email
from auth.infrastructure.persistence.models import UserModel

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

    def delete(self, user: User) -> None:
        user_record = self.session.query(UserModel).filter(UserModel.email == user.email).first()
        if user_record:
            self.session.delete(user_record)
            self.session.commit()


    def update(self, user: User) -> None:
        # Obtener el registro del usuario desde la base de datos
        user_record = self.session.query(UserModel).filter(UserModel.email == user.email).first()
        if user_record:
            # Actualizar todos los atributos relevantes del usuario
            user_record.username = user.username
            user_record.hashed_password = user.password
            user_record.role = user.role
            # Asegurarse de que SQLAlchemy esté detectando los cambios y los confirme
            self.session.commit()
            self.session.refresh(user_record)
