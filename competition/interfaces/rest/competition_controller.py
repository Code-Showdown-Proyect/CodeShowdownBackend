from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from competition.application.commands.create_competition_command import CreateCompetitionCommand
from competition.application.commands.delete_competition_command import DeleteCompetitionCommand
from competition.application.commands.join_competition_command import JoinCompetitionCommand
from competition.application.commands.kick_participant_command import KickParticipantCommand
from competition.application.commands.submit_answer_command import SubmitAnswerCommand
from competition.application.commands.update_competition_command import UpdateCompetitionCommand
from competition.application.handlers.create_competition_handler import CreateCompetitionHandler
from competition.application.handlers.delete_competition_handler import DeleteCompetitionHandler
from competition.application.handlers.join_competition_handler import JoinCompetitionHandler
from competition.application.handlers.kick_participant_handler import KickParticipantHandler
from competition.application.handlers.submit_answer_handler import SubmitAnswerHandler
from competition.application.handlers.update_competition_handler import UpdateCompetitionHandler
from competition.application.services.competition_service import CompetitionService

from competition.infrastructure.persistence.database import SessionLocal
from competition.infrastructure.persistence.sqlalchemy_answer_repository import SQLAlchemyAnswerRepository
from competition.infrastructure.persistence.sqlalchemy_competition_repository import SQLAlchemyCompetitionRepository
from competition.infrastructure.persistence.sqlalchemy_participant_repository import SQLAlchemyParticipantRepository
from pydantic import BaseModel

from competition.security.authorization import get_current_user

router = APIRouter()

class CreateCompetitionRequest(BaseModel):
    name: str
    number_of_exercises: int
    time_limit: int  # en minutos
    password: Optional[str] = None

class JoinCompetitionRequest(BaseModel):
    access_code: str
    password: str = None

class DeleteCompetitionRequest(BaseModel):
    competition_id: int

class SubmitAnswerRequest(BaseModel):
    participant_id: int
    competition_id: int
    exercise_id: int
    answer: str
    time_taken: int

class UpdateCompetitionRequest(BaseModel):
    competition_id: int
    name: str
    number_of_exercises: int
    password: Optional[str] = None

class KickParticipantRequest(BaseModel):
    participant_id: int
    competition_id: int

class UpdateStatus(BaseModel):
    status: str
    competition_id: int

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_competition_service(db: Session = Depends(get_db)):
    competition_repository = SQLAlchemyCompetitionRepository(db)
    participant_repository = SQLAlchemyParticipantRepository(db)
    answer_repository = SQLAlchemyAnswerRepository(db)
    return CompetitionService(competition_repository, participant_repository,answer_repository)



# Endpoint para crear una nueva competencia
@router.post("/create-competition", response_model=dict)
def create_competition(request: CreateCompetitionRequest, service: CompetitionService = Depends(get_competition_service), current_user: int = Depends(get_current_user)):
    print(current_user)
    command = CreateCompetitionCommand(
        name=request.name,
        number_of_exercises=request.number_of_exercises,
        time_limit=request.time_limit,
        password=request.password,
        creator_id=current_user
    )
    handler = CreateCompetitionHandler(service)
    try:
        competition = handler.handle(command)
        return {"message": "Competition created successfully", "access_code": competition.access_code}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Endpoint para unirse a una competencia
@router.post("/join-competition", response_model=dict)
def join_competition(request: JoinCompetitionRequest, service: CompetitionService = Depends(get_competition_service), current_user: int = Depends(get_current_user)):
    command = JoinCompetitionCommand(
        access_code=request.access_code,
        password=request.password,
        user_id= current_user
    )
    handler = JoinCompetitionHandler(service)
    try:
        participant = handler.handle(command)
        return {"message": "Successfully joined competition", "participant_id": participant.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.delete("/delete-competition", response_model=dict)
def delete_competition(request: DeleteCompetitionRequest, service: CompetitionService = Depends(get_competition_service),current_user: int = Depends(get_current_user)):
    command = DeleteCompetitionCommand(
        competition_id=request.competition_id,
        creator_id = current_user
    )
    handler = DeleteCompetitionHandler(service)
    try:
        handler.handle(command)
        return {"message": "Competition deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the creator can delete this competition")

@router.delete("/kick-participant", response_model=dict)
def kick_participant(request: KickParticipantRequest, service: CompetitionService = Depends(get_competition_service),current_user: int = Depends(get_current_user)):
    command = KickParticipantCommand(
        competition_id=request.competition_id,
        creator_id = current_user,
        participant_id=request.participant_id
    )
    handler = KickParticipantHandler(service)
    try:
        handler.handle(command)
        return {"message": "Participant kicked successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the creator can kick participants")


@router.post("/submit-answer", response_model=dict)

def submit_answer(request: SubmitAnswerRequest, service: CompetitionService = Depends(get_competition_service)):
    command = SubmitAnswerCommand(
        participant_id=request.participant_id,
        competition_id=request.competition_id,
        exercise_id=request.exercise_id,
        answer=request.answer,
        time_taken=request.time_taken
    )
    handler = SubmitAnswerHandler(service)
    try:
        handler.handle(command)
        return {"message": "Answer submitted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/update-competition", response_model=dict)
def update_competition(request: UpdateCompetitionRequest, service: CompetitionService = Depends(get_competition_service),current_user: int = Depends(get_current_user)):
    command = UpdateCompetitionCommand(
        competition_id=request.competition_id,
        name=request.name,
        start_date=datetime.utcnow(),
        number_of_exercises=request.number_of_exercises,
        password=request.password,
        creator_id = current_user
    )
    handler = UpdateCompetitionHandler(service)
    try:
        handler.handle(command)
        return {"message": "Competition updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the creator can update this competition")

@router.put("/update-status", response_model=dict)
def update_status(request: UpdateStatus, service: CompetitionService = Depends(get_competition_service)):
    try:
        service.update_status(request.competition_id, request.status)
        return {"message": "Status updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/get-competitions/{accessCode}", response_model=dict)
def get_competitions_by_accessCode(accessCode: str, service: CompetitionService = Depends(get_competition_service)):
    try:
        competitions = service.get_competition_by_accessCode(accessCode)
        return  {
            "competition_id": competitions.id,
            "name": competitions.name,
            "number_of_exercises": competitions.number_of_exercises,
            "time_limit": competitions.time_limit,
            "creator_id": competitions.creator_id
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/get-participants/{competition_id}", response_model=dict)
def get_participants(competition_id: int, service: CompetitionService = Depends(get_competition_service)):
    try:
        participants = service.get_participants(competition_id)
        return {"participants": participants}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/leave-competition/{accessCode}", response_model=dict)
def leave_competition(accessCode: str, service: CompetitionService = Depends(get_competition_service), current_user: int = Depends(get_current_user)):
    try:

        competition = service.get_competition_by_accessCode(accessCode)
        print(current_user)
        print(competition.id)
        service.leave_competition(current_user,competition.id)

        return {"message": "Participant left competition successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/get-participant/{user_id}/{competition_id}", response_model=dict)
def get_participant_by_user_and_competition(user_id: int, competition_id: int, service: CompetitionService = Depends(get_competition_service)):
    try:
        participant = service.participant_repository.find_by_user_and_competition(user_id, competition_id)
        return {
            "participant_id": participant.id,
            "user_id": participant.user_id,
            "competition_id": participant.competition_id,
            "score": participant.score,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))