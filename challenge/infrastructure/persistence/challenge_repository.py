from sqlalchemy.orm import Session
from challenge.domain.repositories.challenge_repository import ChallengeRepository
from challenge.domain.entities.challenge import Challenge
from challenge.infrastructure.persistence.models import ChallengeModel

class SQLAlchemyChallengeRepository(ChallengeRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, challenge_id: str) -> Challenge:
        challenge_record = self.session.query(ChallengeModel).filter(ChallengeModel.id == challenge_id).first()
        if challenge_record:
            return Challenge(
                id=challenge_record.id,
                competition_id=challenge_record.competition_id,
                title=challenge_record.title,
                description=challenge_record.description,
                difficulty=challenge_record.difficulty,
                tags=challenge_record.tags,
                created_at=challenge_record.created_at,
                output_example=challenge_record.output_example
            )
        return None

    def save(self, challenge: Challenge) -> None:
        challenge_model = ChallengeModel(
            title=challenge.title,
            competition_id=challenge.competition_id,
            description=challenge.description,
            difficulty=challenge.difficulty,
            tags=challenge.tags,
            output_example=challenge.output_example
        )
        self.session.add(challenge_model)
        self.session.commit()
        self.session.refresh(challenge_model)
        challenge.id = challenge_model.id

    def list_all(self) -> list:
        challenges = self.session.query(ChallengeModel).all()
        return [
            Challenge(
                id=challenge.id,
                competition_id= challenge.competition_id,
                title=challenge.title,
                description=challenge.description,
                difficulty=challenge.difficulty,
                tags=challenge.tags,
                created_at=challenge.created_at,
                output_example=challenge.output_example
            ) for challenge in challenges
        ]

    def delete(self, challenge_id: str) -> bool:
        challenge_record = self.session.query(ChallengeModel).filter(ChallengeModel.id == challenge_id).first()
        if challenge_record:
            self.session.delete(challenge_record)
            self.session.commit()
            return True
        return False