from competition.domain.entities.competition import Competition
from competition.domain.entities.participant import Participant
from competition.domain.repositories.competition_repository import CompetitionRepository
from competition.domain.repositories.participant_repository import ParticipantRepository
from datetime import datetime
from typing import Optional

class CompetitionService:
    def __init__(self, competition_repository: CompetitionRepository, participant_repository: ParticipantRepository):
        self.competition_repository = competition_repository
        self.participant_repository = participant_repository

    def create_competition(self, name: str, number_of_exercises: int, time_limit: int, creator_id: int, password: Optional[str] = None) -> Competition:
        competition = Competition(
            id=None,
            name=name,
            number_of_exercises=number_of_exercises,
            time_limit=time_limit,
            created_at=datetime.utcnow(),
            status="pending",
            access_code=self._generate_access_code(),
            password=password,
            creator_id= creator_id
        )
        self.competition_repository.create(competition)
        return competition

    def get_competition_by_id(self, competition_id: int) -> Competition:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        return competition

    def generate_first_challenge(self, competition_id: int):
        competition = self.get_competition_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")

        # Aquí podrías integrar la lógica del contexto de generación de desafíos (por ejemplo, `ChallengeGeneration`).
        # O generar un desafío de prueba para el primer desafío.
        first_challenge = {
            "id": 1,
            "title": "Primer Desafío de Competencia",
            "description": "Implementa una función que devuelva el número factorial de un entero positivo.",
            "difficulty": "media"
        }
        return first_challenge


    def join_competition(self, access_code: str, user_id: int, password: Optional[str] = None) -> Participant:
        competition = self.competition_repository.find_by_access_code(access_code)
        if not competition:
            raise ValueError("Competition not found")
        if competition.password and competition.password != password:
            raise PermissionError("Incorrect password")

        participant = Participant(
            id=None,
            user_id=user_id,  
            competition_id=competition.id,
            joined_at=datetime.utcnow(),
            score=0
        )
        self.participant_repository.create(participant)
        return participant

    def submit_answer(self, participant_id: int, competition_id: int, answer: str, time_taken: int) -> None:
        """Recibe la respuesta de un participante y almacena la información sin evaluar"""
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")

        participant = self.participant_repository.find_by_id(participant_id)
        if not participant:
            raise ValueError("Participant not found")

        # Aquí, simplemente almacenamos la respuesta junto con el tiempo tomado para futuras evaluaciones
        self._store_answer(participant_id, competition_id, answer, time_taken)

    def _store_answer(self, participant_id: int, competition_id: int, answer: str, time_taken: int) -> None:
        """Almacena la respuesta y el tiempo tomado en algún repositorio específico"""
        # Aquí deberíamos tener un repositorio que almacene las respuestas.
        # Esto podría ser implementado en el futuro como AnswerRepository.
        print(f"Respuesta del participante {participant_id} en competencia {competition_id} almacenada.")

    def _generate_access_code(self) -> str:
        # Lógica para generar un código de acceso único (por ejemplo, alfanumérico de 6 caracteres)
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def delete_competition(self, competition_id, creator_id)->None:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        if competition.creator_id != creator_id:
            raise PermissionError("Only the creator can delete this competition")

        participants = self.participant_repository.find_by_competition_id(competition_id)
        for participant in participants:
            self.participant_repository.delete(participant.id)
        self.competition_repository.delete(competition_id)
