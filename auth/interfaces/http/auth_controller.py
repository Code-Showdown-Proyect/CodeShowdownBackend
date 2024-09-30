from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.application.services import AuthService
from auth.domain.value_objects import Email
from auth.infrastructure.persistence.database import SessionLocal
from auth.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from auth.application.commands import RegisterUserCommand, AuthenticateUserCommand
from auth.application.handlers import RegisterUserHandler, AuthenticateUserHandler
from pydantic import BaseModel

router = APIRouter()

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdatePasswordRequest(BaseModel):
    email: str
    current_password: str
    new_password: str

class UpdateUsernameRequest(BaseModel):
    email: str
    new_username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_register_user_handler(db: Session = Depends(get_db)):
    user_repository = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repository)
    return RegisterUserHandler(auth_service)

def get_authenticate_user_handler(db: Session = Depends(get_db)):
    user_repository = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repository)
    return AuthenticateUserHandler(auth_service)

@router.post("/register", response_model=dict)
def register(request: RegisterUserRequest, handler: RegisterUserHandler = Depends(get_register_user_handler)):
    command = RegisterUserCommand(
        username=request.username, 
        email=request.email, 
        password=request.password, 
        role ="Basic"
    )
    try:
        new_user = handler.handle(command)
        return {"message": "User registered successfully", "username": new_user.username}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=dict)
def login(request: LoginRequest, handler: AuthenticateUserHandler = Depends(get_authenticate_user_handler)):
    command = AuthenticateUserCommand(
        email=request.email,
        password=request.password
    )
    access_token = handler.handle(command)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/update-password", response_model=dict)
def update_password(request: UpdatePasswordRequest, handler: RegisterUserHandler = Depends(get_register_user_handler)):
    email_obj = Email(request.email)
    success = handler.auth_service.update_password(email_obj, request.current_password, request.new_password)
    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect or user not found")
    return {"message": "Password updated successfully"}

@router.put("/update-username", response_model=dict)
def update_username(request: UpdateUsernameRequest, handler: RegisterUserHandler = Depends(get_register_user_handler)):
    email_obj = Email(request.email)
    updated_user = handler.auth_service.update_username(email_obj, request.new_username)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Username updated successfully", "new_username": updated_user.username}