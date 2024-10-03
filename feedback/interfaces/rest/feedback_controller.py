from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from feedback.application.services.feedback_service import FeedbackService
from feedback.application.commands.analyze_response_command import AnalyzeResponseCommand
from feedback.application.handlers.analyze_response_handler import AnalyzeResponseHandler
from feedback.infrastructure.database import SessionLocal
from feedback.infrastructure.persistence.sqlalchemy_feedback_repository import SQLAlchemyFeedbackRepository
from feedback.infrastructure.persistence.sqlalchemy_response_repository import SQLAlchemyResponseRepository
from pydantic import BaseModel

from feedback.security.authorization import get_current_user

router = APIRouter()


# Clase para solicitar el análisis de una respuesta
class AnalyzeResponseRequest(BaseModel):
    participant_id: int

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_feedback_service():
    db = SessionLocal()
    try:
        response_repository = SQLAlchemyResponseRepository(db)
        feedback_repository = SQLAlchemyFeedbackRepository(db)
        return FeedbackService(response_repository, feedback_repository)
    finally:
        db.close()


# Endpoint para generar la retroalimentación para una respuesta específica
@router.post("/analyze-response", response_model=dict)
def analyze_response(request: AnalyzeResponseRequest, service: FeedbackService = Depends(get_feedback_service)):
    command = AnalyzeResponseCommand(participant_id=request.participant_id)
    handler = AnalyzeResponseHandler(service)
    try:
        feedbacks = handler.handle(command)
        if feedbacks:
            return {
                "message": "Feedback generated successfully",
                "feedbacks": [
                    {
                        "feedback_id": feedback.id,  # Asegúrate de que este atributo existe
                        "content": feedback.detail,  # Cambia a detail si es necesario
                        "is_correct": feedback.is_correct,
                        "score": feedback.score
                    }
                    for feedback in feedbacks
                ]
            }
        else:
            raise ValueError("No feedback generated.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Clase para obtener la retroalimentación por response_id
class GetFeedbackRequest(BaseModel):
    response_id: int

# Endpoint para obtener la retroalimentación de una respuesta
@router.get("/get-feedback/{response_id}", response_model=dict)
def get_feedback(response_id: int, service: FeedbackService = Depends(get_feedback_service)):
    feedback = service.get_feedback_by_response_id(response_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return {
        "feedback_id": feedback.id,
        "content": feedback.content,
        "is_correct": feedback.is_correct,
        "score": feedback.score
    }