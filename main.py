"""from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}"""
from datetime import datetime
import asyncio


"""from auth.domain.entities import User
from auth.domain.value_objects import Email
from auth.infrastructure.persistence.database import init_db, SessionLocal
from auth.infrastructure.repositories.user_repository import SQLAlchemyUserRepository


def main():
    init_db()
    session = SessionLocal()
    try:
        user_repository = SQLAlchemyUserRepository(session)

        new_user = User(
            id = None,
            username="testuser",
            email="testuser@example.com",
            password="hashedpassword123",
            role="basic"
        )

        user_repository.create(new_user)
        user = user_repository.find_by_email(Email("testuser@example.com"))
        print(f"Usuario encontrado: {user}")
    finally:
        session.close()


if __name__ == '__main__':
    main()"""
from fastapi import FastAPI
from auth.interfaces.http.auth_controller import router as auth_router
from challenge.interfaces.rest.challenge_controller import router as challenge_router
from competition.interfaces.web_sockets.competition_socket import router as competition_socket_router
from competition.interfaces.rest.competition_controller import router as competition_controller_router
from feedback.interfaces.rest.feedback_controller import router as feedback_controller_router
from user_profile.interfaces.http.user_profile_controller import router as profile_controller_router

app = FastAPI()

# Incluir las rutas de autenticación en la aplicación
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(challenge_router, prefix="/challenges", tags=["challenges"])
app.include_router(competition_socket_router, prefix="/ws", tags=["websockets"])
app.include_router(competition_controller_router, prefix="/competitions")
app.include_router(feedback_controller_router, prefix="/feedback")
app.include_router(profile_controller_router, prefix="/profile")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
