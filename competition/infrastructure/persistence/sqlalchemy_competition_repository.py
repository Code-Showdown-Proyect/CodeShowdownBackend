from typing import Optional, List
from sqlalchemy.orm import Session
from competition.domain.entities.competition import Competition
from competition.domain.repositories.competition_repository import CompetitionRepository
from competition.infrastructure.persistence.models import CompetitionModel

class SQLAlchemyCompetitionRepository(CompetitionRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, competition: Competition) -> None:
        """Crea una nueva competencia en la base de datos"""
        competition_model = CompetitionModel(
            name=competition.name,
            number_of_exercises=competition.number_of_exercises,
            time_limit=competition.time_limit,
            created_at=competition.created_at,
            status=competition.status,
            creator_id=competition.creator_id,
            access_code=competition.access_code,
            password=competition.password
        )
        self.session.add(competition_model)
        self.session.commit()
        self.session.refresh(competition_model)
        competition.id = competition_model.id

    def find_by_id(self, competition_id: int) -> Optional[Competition]:
        """Busca una competencia por su ID"""
        competition_model = self.session.query(CompetitionModel).filter_by(id=competition_id).first()
        if not competition_model:
            return None
        return self._to_entity(competition_model)

    def find_by_access_code(self, access_code: str) -> Optional[Competition]:
        """Busca una competencia por su código de acceso"""
        competition_model = self.session.query(CompetitionModel).filter_by(access_code=access_code).first()
        if not competition_model:
            return None
        return self._to_entity(competition_model)

    def list_all(self) -> List[Competition]:
        """Lista todas las competencias disponibles"""
        competition_models = self.session.query(CompetitionModel).all()
        return [self._to_entity(model) for model in competition_models]

    def update(self, competition: Competition) -> None:
        """Actualiza una competencia existente"""
        competition_model = self.session.query(CompetitionModel).filter_by(id=competition.id).first()
        if competition_model:
            competition_model.name = competition.name
            competition_model.number_of_exercises = competition.number_of_exercises
            competition_model.time_limit = competition.time_limit
            competition_model.status = competition.status
            competition_model.password = competition.password
            self.session.commit()
            self.session.refresh(competition_model)

    def delete(self, competition_id: int) -> None:
        """Elimina una competencia de la base de datos"""
        competition_model = self.session.query(CompetitionModel).filter_by(id=competition_id).first()
        if competition_model:
            self.session.delete(competition_model)
            self.session.commit()

    def _to_entity(self, model: CompetitionModel) -> Competition:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio"""
        return Competition(
            id=model.id,
            name=model.name,
            number_of_exercises=model.number_of_exercises,
            time_limit=model.time_limit,
            created_at=model.created_at,
            status=model.status,
            creator_id=model.creator_id,
            access_code=model.access_code,
            password=model.password
        )