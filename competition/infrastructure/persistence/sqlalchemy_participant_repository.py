from typing import Optional, List
from sqlalchemy.orm import Session
from competition.domain.entities.participant import Participant
from competition.domain.repositories.participant_repository import ParticipantRepository
from competition.infrastructure.persistence.models import ParticipantModel

class SQLAlchemyParticipantRepository(ParticipantRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, participant: Participant) -> None:
        """Crea un nuevo participante en la base de datos"""
        participant_model = ParticipantModel(
            user_id=participant.user_id,
            competition_id=participant.competition_id,
            score=participant.score,
            joined_at=participant.joined_at
        )
        self.session.add(participant_model)
        self.session.commit()
        self.session.refresh(participant_model)
        participant.id = participant_model.id

    def find_by_id(self, participant_id: int) -> Optional[Participant]:
        """Busca un participante por su ID"""
        participant_model = self.session.query(ParticipantModel).filter_by(id=participant_id).first()
        if not participant_model:
            return None
        return self._to_entity(participant_model)

    def list_by_competition(self, competition_id: int) -> List[Participant]:
        """Lista todos los participantes de una competencia específica"""
        participant_models = self.session.query(ParticipantModel).filter_by(competition_id=competition_id).all()
        return [self._to_entity(model) for model in participant_models]

    def update(self, participant: Participant) -> None:
        """Actualiza la información de un participante"""
        participant_model = self.session.query(ParticipantModel).filter_by(id=participant.id).first()
        if participant_model:
            participant_model.score = participant.score
            self.session.commit()
            self.session.refresh(participant_model)

    def delete(self, participant_id: int) -> None:
        """Elimina un participante de la base de datos"""
        participant_model = self.session.query(ParticipantModel).filter_by(id=participant_id).first()
        if participant_model:
            self.session.delete(participant_model)
            self.session.commit()

    def _to_entity(self, model: ParticipantModel) -> Participant:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio"""
        return Participant(
            id=model.id,
            user_id=model.user_id,
            competition_id=model.competition_id,
            score=model.score,
            joined_at=model.joined_at
        )

    def find_by_competition_id(self, competition_id: int) -> list:
        return self.session.query(ParticipantModel).filter_by(competition_id=competition_id).all()

    def find_by_user_and_competition(self, user_id: int, competition_id: int) -> Participant:
        participant_model = self.session.query(ParticipantModel).filter_by(user_id=user_id, competition_id=competition_id).first()
        if not participant_model:
            return None
        return self._to_entity(participant_model)