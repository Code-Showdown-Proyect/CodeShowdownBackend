# Manejadores de comandos y eventos.
from auth.application.commands import RegisterUserCommand, AuthenticateUserCommand
from auth.application.services import AuthService
from auth.domain.entities import User
from typing import Optional
from auth.domain.value_objects import Email


class RegisterUserHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def handle(self, command: RegisterUserCommand) -> User:
        return self.auth_service.register_user(
            username=command.username,
            email=command.email,
            password=command.password
        )

class AuthenticateUserHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def handle(self, command: AuthenticateUserCommand) -> Optional[str]:
        user = self.auth_service.authenticate_user(
            email=Email(command.email),
            password=command.password
        )
        if user:
            access_token = self.auth_service.create_access_token(data={"sub": user.email})
            return access_token
        return None