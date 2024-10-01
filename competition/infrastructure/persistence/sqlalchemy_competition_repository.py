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
        try:
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
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear la competencia: {e}")

    def find_by_id(self, competition_id: int) -> Optional[Competition]:
        """Busca una competencia por su ID"""
        try:
            competition_model = self.session.query(CompetitionModel).filter_by(id=competition_id).first()
            if competition_model is None:
                return None
            return self._to_entity(competition_model)
        except Exception as e:
            # Manejo de errores o logueo puede ser agregado aquí
            print(f"Error occurred: {e}")
            return None

    def find_by_access_code(self, access_code: str) -> Optional[Competition]:
        """Busca una competencia por su código de acceso"""
        try:
            competition_model = self.session.query(CompetitionModel).filter_by(access_code=access_code).first()
            if not competition_model:
                return None
            return self._to_entity(competition_model)
        except Exception as e:
            # Manejar la excepción de acceso a la base de datos aquí
            print(f"Error buscando competencia con código de acceso {access_code}: {e}")
            return None

    def list_all(self) -> List[Competition]:
        """Lista todas las competencias disponibles"""
        try:
            competition_models = self.session.query(CompetitionModel).all()
            return [self._to_entity(model) for model in competition_models]
        except Exception as e:
            # Manejo de excepción específico según sea necesario
            print(f"Error al listar todas las competencias: {e}")
            return []

    def update(self, competition: Competition) -> None:
        """Actualiza una competencia existente"""
        try:
            # Obtener el modelo de la competencia
            competition_model = self.session.query(CompetitionModel).filter_by(id=competition.id).first()

            # Confirmar que la competencia existe
            if competition_model:
                # Validar y actualizar los campos necesarios
                if competition.name:
                    competition_model.name = competition.name
                if competition.number_of_exercises is not None:
                    competition_model.number_of_exercises = competition.number_of_exercises
                if competition.time_limit is not None:
                    competition_model.time_limit = competition.time_limit
                if competition.status:
                    competition_model.status = competition.status
                if competition.password is not None:
                    competition_model.password = competition.password

                # Confirmar y refrescar la transacción
                self.session.commit()
                self.session.refresh(competition_model)
            else:
                print(f"Competition with id {competition.id} not found.")

        except Exception as e:
            # Capturar y manejar excepciones
            self.session.rollback()
            print(f"An error occurred during the update: {str(e)}")

    def delete(self, competition_id: int) -> None:
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
