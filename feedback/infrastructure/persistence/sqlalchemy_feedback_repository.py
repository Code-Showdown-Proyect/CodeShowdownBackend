from sqlalchemy.orm import Session
from feedback.domain.repositories.feedback_repository import FeedbackRepository
from feedback.infrastructure.persistence.models import FeedbackModel
from feedback.domain.entities.feedback import Feedback
from typing import Optional

class SQLAlchemyFeedbackRepository(FeedbackRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, feedback: Feedback) -> None:
        """Guarda la retroalimentación en la base de datos, creando o actualizando."""
        if feedback.id is None:
            # Crear nueva retroalimentación
            feedback_model = FeedbackModel(
                response_id=feedback.response_id,
                detail=feedback.detail,
                score=feedback.score,
                is_correct=feedback.is_correct
            )
            self.session.add(feedback_model)
            self.session.commit()
            self.session.refresh(feedback_model)
            feedback.id = feedback_model.id
        else:
            # Actualizar retroalimentación existente
            feedback_model = self.session.query(FeedbackModel).filter_by(id=feedback.id).first()
            if feedback_model:
                feedback_model.content = feedback.detail
                feedback_model.score = feedback.score
                feedback_model.is_correct = feedback.is_correct
                self.session.commit()

    def find_by_response_id(self, response_id: int) -> Optional[FeedbackModel]:
        """Encuentra la retroalimentación asociada a una respuesta específica."""
        return self.session.query(FeedbackModel).filter_by(response_id=response_id).first()

    def delete(self, feedback_id: int) -> None:
        """Elimina una retroalimentación de la base de datos."""
        feedback = self.session.query(FeedbackModel).filter_by(id=feedback_id).first()
        if feedback:
            self.session.delete(feedback)
            self.session.commit()