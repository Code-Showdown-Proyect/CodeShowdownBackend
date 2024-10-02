from challenge.domain.entities.challenge import Challenge
from challenge.infrastructure.external.chatgpt_api import ChatGPTClient


class ChallengeService:
    def __init__(self, challenge_repository):
        self.challenge_repository = challenge_repository
        self.chatgpt_client = ChatGPTClient()

    def generate_challenge(self, difficulty: str, topic: str, competition_id: int)-> Challenge:

        challenge_text, output_example = self.chatgpt_client.generate_challenge(difficulty, topic)

        challenge = Challenge(
            id=None,
            competition_id = competition_id,
            title=f"Reto de {topic} ({difficulty})",
            description=challenge_text,
            difficulty=difficulty,
            tags=[topic],
            created_at=None,
            output_example=output_example
        )
        self.challenge_repository.save(challenge)
        return challenge

    def get_challenge_by_id(self, challenge_id: str) -> Challenge:
        challenge = self.challenge_repository.find_by_id(challenge_id)
        if challenge is None:
            raise ValueError("Challenge not found")
        return challenge

    def list_all_challenges(self) -> list:
        return self.challenge_repository.list_all()

    def delete_challenge(self, challenge_id: str) -> bool:
        return self.challenge_repository.delete(challenge_id)

    def list_all_challenges_by_competition_id(self, competition_id):
        return self.challenge_repository.list_all_by_competition_id(competition_id)



