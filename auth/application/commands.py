# Definición de comandos que se pueden ejecutar, como RegisterUserCommand.

from dataclasses import dataclass


@dataclass
class RegisterUserCommand:
    username: str
    email: str
    password: str
    role: str

@dataclass
class AuthenticateUserCommand:
    email: str
    password: str