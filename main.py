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

from Auth.domain.entities import User
from Auth.domain.value_objects import Email
from Auth.infrastructure.persistence.database import init_db, SessionLocal
from Auth.infrastructure.repositories.user_repository import SQLAlchemyUserRepository


def main():
    init_db()
    session = SessionLocal()
    try:
        user_repository = SQLAlchemyUserRepository(session)

        new_user = User(

            username="testuser",
            email="testuser@example.com",
            hashed_password="hashedpassword123",
            role="basic",
            created_at=datetime.utcnow()
        )

        user_repository.create(new_user)
        user = user_repository.find_by_email(Email("testuser@example.com"))
        print(f"Usuario encontrado: {user}")
    finally:
        session.close()


if __name__ == '__main__':
    main()