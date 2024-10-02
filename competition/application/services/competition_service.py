import httpx

from competition.domain.entities.answer import Answer
from competition.domain.entities.competition import Competition
from competition.domain.entities.participant import Participant
from competition.domain.repositories.competition_repository import CompetitionRepository
from competition.domain.repositories.participant_repository import ParticipantRepository
from competition.domain.repositories.answer_repository import AnswerRepository
from datetime import datetime
from typing import Optional

class CompetitionService:
    def __init__(self, competition_repository: CompetitionRepository, participant_repository: ParticipantRepository, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository
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

    async def generate_first_challenge(self, competition_id: int):
        competition = self.get_competition_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")

        # URL del endpoint del microservicio de challenges
        challenge_service_url = f"http://127.0.0.1:8000/challenges/get-challenges-by-competition/{competition_id}"

        # Realizar la solicitud HTTP al microservicio
        async with httpx.AsyncClient() as client:
            response = await client.get(challenge_service_url)

        # Validar la respuesta
        if response.status_code != 200:
            raise ValueError("Failed to fetch challenges from Challenge Service")

        challenges = response.json()
        if not challenges:
            raise ValueError("No challenges found for this competition")
        # Aquí podrías integrar la lógica del contexto de generación de desafíos (por ejemplo, `ChallengeGeneration`).
        # O generar un desafío de prueba para el primer desafío.
        first_challenge = challenges[0]
        print(challenges)
        print("First challenge:", first_challenge)

        return{
            "id": first_challenge["id"],
            "title": first_challenge["title"],
            "description": first_challenge["description"],
            "difficulty": first_challenge["difficulty"]
        }


    def join_competition(self, access_code: str, user_id: int, password: Optional[str] = None) -> Participant:
        competition = self.competition_repository.find_by_access_code(access_code)
        if not competition:
            raise ValueError("Competition not found")
        if competition.password and competition.password != password:
            raise PermissionError("Incorrect password")
        existing_participant = self.participant_repository.find_by_user_and_competition(user_id, competition.id)
        if existing_participant:
            raise ValueError("User is already joined in this competition")
        participant = Participant(
            id=None,
            user_id=user_id,  
            competition_id=competition.id,
            joined_at=datetime.utcnow(),
            score=0
        )
        self.participant_repository.create(participant)
        return participant

    def submit_answer(self, participant_id: int, competition_id: int, answer: str, time_taken: int, exercise_id: int) -> Answer:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        participant = self.participant_repository.find_by_id(participant_id)
        if not participant:
            raise ValueError("Participant not found")
        answer = Answer(
            id=None,
            participant_id=participant_id,
            challenge_id=exercise_id,
            answer=answer,
            time_taken=time_taken
        )
        self.answer_repository.create(answer)
        return answer

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

    def kick_participant(self, participant_id: int, competition_id: int, creator_id: int) -> None:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        if competition.creator_id != creator_id:
            raise PermissionError("Only the creator can kick the participant")
        participants = self.participant_repository.find_by_competition_id(competition_id)
        for participant in participants:
            if participant.id == participant_id:
                self.participant_repository.delete(participant.id)
            if participant_id not in [p.id for p in participants]:
                raise ValueError("Participant not found in competition")

    def update_competition(self, competition_id, creator_id, name, number_of_exercises, time_limit, password)->Competition:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        if competition.creator_id != creator_id:
            raise PermissionError("Only the creator can update this competition")
        competition.name = name
        competition.number_of_exercises = number_of_exercises
        competition.time_limit = time_limit
        competition.password = password
        self.competition_repository.update(competition)
        return competition

    def update_status(self, competition_id, status)->Competition:
        competition = self.competition_repository.find_by_id(competition_id)
        if not competition:
            raise ValueError("Competition not found")
        competition.status = status
        self.competition_repository.update(competition)
        return competition