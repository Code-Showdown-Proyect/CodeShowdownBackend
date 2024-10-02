from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.infrastructure.persistence.database import SessionLocal
from challenge.application.services.challenge_service import ChallengeService

from challenge.application.commands.generate_challenge_command import GenerateChallengeCommand
from challenge.application.handlers.generate_challenge_handler import GenerateChallengeHandler
from challenge.infrastructure.persistence.sqlalchemy_challenge_repository import SQLAlchemyChallengeRepository

router = APIRouter()

class ChallengeResponse(BaseModel):
    id: int
    competition_id:int
    title: str
    description: str
    difficulty: str
    tags: List[str]
    output_example: str

class GenerateChallengeRequest(BaseModel):
    difficulty: str
    topic: str
    competition_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_challenge_service(db: Session = Depends(get_db)):
    challenge_repository = SQLAlchemyChallengeRepository(db)
    return ChallengeService(challenge_repository)


from fastapi import APIRouter, Depends, HTTPException, status, Body

@router.post("/generate-challenge", response_model=ChallengeResponse)
def generate_challenge(generate_request: GenerateChallengeRequest = Body(...), service: ChallengeService = Depends(get_challenge_service)):
    try:
        command = GenerateChallengeCommand(difficulty=generate_request.difficulty, topic=generate_request.topic, competition_id= generate_request.competition_id)
        handler = GenerateChallengeHandler(service)
        challenge = handler.handle(command)
        return {
            "id": challenge.id,
            "competition_id": challenge.competition_id,
            "title": challenge.title,
            "description": challenge.description,
            "difficulty": challenge.difficulty,
            "tags": challenge.tags,
            "output_example": challenge.output_example
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/list-challenges", response_model=List[ChallengeResponse])
def list_challenges(service: ChallengeService = Depends(get_challenge_service)):
    try:
        challenges = service.list_all_challenges()
        return [
            {
                "id": challenge.id,
                "competition_id":challenge.competition_id,
                "title": challenge.title,
                "description": challenge.description,
                "difficulty": challenge.difficulty,
                "tags": challenge.tags,
                "output_example": challenge.output_example
            }
            for challenge in challenges
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get-challenge/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: str, service: ChallengeService = Depends(get_challenge_service)):
    try:
        challenge = service.get_challenge_by_id(challenge_id)
        return {
            "id": challenge.id,
            "competition_id": challenge.competition_id,
            "title": challenge.title,
            "description": challenge.description,
            "difficulty": challenge.difficulty,
            "tags": challenge.tags,
            "output_example": challenge.output_example
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-challenges-by-competition/{competition_id}", response_model=List[ChallengeResponse])
def get_challenge(competition_id: str, service: ChallengeService = Depends(get_challenge_service)):
    try:
        challenges = service.list_all_challenges_by_competition_id(competition_id)
        return [
            {
                "id": challenge.id,
                "competition_id": challenge.competition_id,
                "title": challenge.title,
                "description": challenge.description,
                "difficulty": challenge.difficulty,
                "tags": challenge.tags,
                "output_example": challenge.output_example
            }
            for challenge in challenges
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete-challenge/{challenge_id}", response_model=dict)
def delete_challenge(challenge_id: str, service: ChallengeService = Depends(get_challenge_service)):
    try:
        success = service.delete_challenge(challenge_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
        return {"message": "Challenge deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
