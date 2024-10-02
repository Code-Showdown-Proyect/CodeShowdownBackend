from sqlalchemy.orm import Session
from typing import Optional

from feedback.domain.repositories.response_repository import ResponseRepository
from feedback.infrastructure.persistence.models import ResponseModel
from feedback.domain.entities.response import Response  # Suponiendo que esta entidad está definida en el dominio

class SQLAlchemyResponseRepository(ResponseRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, response: Response) -> None:
        """Guarda la respuesta en la base de datos (crea o actualiza)"""
        if response.id is None:
            # Crear nueva respuesta
            response_model = ResponseModel(
                participant_id=response.participant_id,
                challenge_id=response.challenge_id,
                answer=response.answer,
                time_taken=response.time_taken,
                feedback=response.feedback.content if response.feedback else None,
                is_correct=response.feedback.is_correct if response.feedback else None,
                score=response.feedback.score if response.feedback else None
            )
            self.session.add(response_model)
            self.session.commit()
            self.session.refresh(response_model)
            response.id = response_model.id
        else:
            # Actualizar respuesta existente
            response_model = self.session.query(ResponseModel).filter_by(id=response.id).first()
            if response_model:
                response_model.answer = response.answer
                response_model.time_taken = response.time_taken
                if response.feedback:
                    response_model.feedback = response.feedback.content
                    response_model.is_correct = response.feedback.is_correct
                    response_model.score = response.feedback.score
                self.session.commit()

    def find_by_id(self, response_id: int) -> Optional[ResponseModel]:
        """Encuentra la respuesta por su ID"""
        return self.session.query(ResponseModel).filter_by(id=response_id).first()

    def delete(self, response_id: int) -> None:
        """Elimina una respuesta de la base de datos"""
        response = self.find_by_id(response_id)
        if response:
            self.session.delete(response)
            self.session.commit()