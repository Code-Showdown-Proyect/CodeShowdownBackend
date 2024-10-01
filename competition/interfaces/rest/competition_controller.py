from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from competition.application.commands.create_competition_command import CreateCompetitionCommand
from competition.application.commands.delete_competition_command import DeleteCompetitionCommand
from competition.application.commands.join_competition_command import JoinCompetitionCommand
from competition.application.commands.submit_answer_command import SubmitAnswerCommand
from competition.application.handlers.create_competition_handler import CreateCompetitionHandler
from competition.application.handlers.delete_competition_handler import DeleteCompetitionHandler
from competition.application.handlers.join_competition_handler import JoinCompetitionHandler
from competition.application.handlers.submit_answer_handler import SubmitAnswerHandler
from competition.application.services.competition_service import CompetitionService

from competition.infrastructure.persistence.database import SessionLocal
from competition.infrastructure.persistence.sqlalchemy_competition_repository import SQLAlchemyCompetitionRepository
from competition.infrastructure.persistence.sqlalchemy_participant_repository import SQLAlchemyParticipantRepository
from pydantic import BaseModel

router = APIRouter()

class CreateCompetitionRequest(BaseModel):
    name: str
    number_of_exercises: int
    time_limit: int  # en minutos
    password: str = None

class JoinCompetitionRequest(BaseModel):
    access_code: str
    password: str = None

class DeleteCompetitionRequest(BaseModel):
    competition_id: int

class SubmitAnswerRequest(BaseModel):
    participant_id: int
    competition_id: int
    answer: str
    time_taken: int

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
    return CompetitionService(competition_repository, participant_repository)

# Endpoint para crear una nueva competencia
@router.post("/create-competition", response_model=dict)
def create_competition(request: CreateCompetitionRequest, service: CompetitionService = Depends(get_competition_service)):
    command = CreateCompetitionCommand(
        name=request.name,
        number_of_exercises=request.number_of_exercises,
        time_limit=request.time_limit,
        password=request.password
    )
    handler = CreateCompetitionHandler(service)
    try:
        competition = handler.handle(command)
        return {"message": "Competition created successfully", "access_code": competition.access_code}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Endpoint para unirse a una competencia
@router.post("/join-competition", response_model=dict)
def join_competition(request: JoinCompetitionRequest, service: CompetitionService = Depends(get_competition_service)):
    command = JoinCompetitionCommand(
        access_code=request.access_code,
        password=request.password
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

def delete_competition(request: DeleteCompetitionRequest, service: CompetitionService = Depends(get_competition_service)):
    command = DeleteCompetitionCommand(competition_id=request.competition_id)
    handler = DeleteCompetitionHandler(service)
    try:
        handler.handle(command)
        return {"message": "Competition deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
@router.post("/submit-answer", response_model=dict)

def submit_answer(request: SubmitAnswerRequest, service: CompetitionService = Depends(get_competition_service)):
    command = SubmitAnswerCommand(
        participant_id=request.participant_id,
        competition_id=request.competition_id,
        answer=request.answer,
        time_taken=request.time_taken
    )
    handler = SubmitAnswerHandler(service)
    try:
        handler.handle(command)
        return {"message": "Answer submitted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))