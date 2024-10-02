from sqlalchemy.orm import Session

from competition.domain.entities.answer import Answer
from competition.domain.repositories.answer_repository import AnswerRepository
from competition.infrastructure.persistence.models import AnswerModel


class SQLAlchemyAnswerRepository(AnswerRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, answer: Answer) -> None:
        """Crea una nueva competencia en la base de datos"""
        try:
            answer_model = AnswerModel(
                participant_id=answer.participant_id,
                challenge_id=answer.challenge_id,
                answer=answer.answer,
                time_taken=answer.time_taken
            )
            self.session.add(answer_model)
            self.session.commit()
            self.session.refresh(answer_model)
            answer.id = answer_model.id
        except Exception as e:
            self.session.rollback()
            print(f"Error al enviar la respuesta: {e}")
