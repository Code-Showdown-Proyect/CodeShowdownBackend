# Controladores que manejan las solicitudes HTTP (registro, login).

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.application.services import AuthService
from auth.infrastructure.persistence.database import SessionLocal
from auth.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from auth.application.commands import RegisterUserCommand, AuthenticateUserCommand
from auth.application.handlers import RegisterUserHandler, AuthenticateUserHandler

# Crear el router para las rutas de autenticación
router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia para obtener los servicios y manejadores
def get_register_user_handler(db: Session = Depends(get_db)):
    user_repository = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repository)
    return RegisterUserHandler(auth_service)

def get_authenticate_user_handler(db: Session = Depends(get_db)):
    user_repository = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repository)
    return AuthenticateUserHandler(auth_service)

# Ruta para el registro de usuarios
@router.post("/register", response_model=dict)
def register(username: str, email: str, password: str, handler: RegisterUserHandler = Depends(get_register_user_handler)):
    command = RegisterUserCommand(username=username, email=email, password=password)
    try:
        new_user = handler.handle(command)
        return {"message": "User registered successfully", "username": new_user.username}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Ruta para el inicio de sesión
@router.post("/login", response_model=dict)
def login(email: str, password: str, handler: AuthenticateUserHandler = Depends(get_authenticate_user_handler)):
    command = AuthenticateUserCommand(email=email, password=password)
    access_token = handler.handle(command)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"access_token": access_token, "token_type": "bearer"}