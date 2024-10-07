from sqlalchemy.orm import Session
from typing import Optional, List, Type

from feedback.domain.repositories.response_repository import ResponseRepository
from feedback.infrastructure.persistence.models import ResponseModel, ParticipantModel, ChallengeModel
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

    def find_by_id(self, participant_id: int) -> list[Type[ResponseModel]]:
        """Encuentra todas las respuestas por el ID del participante y devuelve una lista."""
        return self.session.query(ResponseModel).filter(ResponseModel.participant_id == participant_id).all()

    def delete(self, response_id: int) -> None:
        """Elimina una respuesta de la base de datos"""
        response = self.find_by_id(response_id)
        if response:
            self.session.delete(response)
            self.session.commit()
    def update_response_with_feedback(self, participant_id: int, feedback: str, is_correct: bool)-> None:
        """Actualiza una respuesta con la retroalimentación generada"""
        response = self.session.query(ResponseModel).filter_by(participant_id=participant_id).first()
        # Verificar si se encontró la respuesta
        if response is None:
            print(f"No se encontró ninguna respuesta para el participante con id {participant_id}")
            return  # Podrías manejarlo de otra manera, como lanzar una excepción o registrar un log
        if response:
            response.feedback = feedback
            response.is_correct = is_correct
            self.session.commit()

    def update_score(self, participant_id: int, scores: list[int])-> None:
        """Actualiza el puntaje de una respuesta"""
        response = self.session.query(ParticipantModel).filter_by(id=participant_id).first()
        total_score = sum(scores)
        if response:
            response.score = total_score
            self.session.commit()

    def find_question_by_id(self, challenge_id: int )-> Type[ChallengeModel] | None:
        """Encuentra la pregunta por su ID"""
        question = self.session.query(ChallengeModel).filter_by(id=challenge_id).first()
        return question