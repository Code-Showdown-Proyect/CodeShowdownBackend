from challenge.application.commands.generate_challenge_command import GenerateChallengeCommand
from challenge.application.services.challenge_service import ChallengeService


class GenerateChallengeHandler:
    def __init__(self, challenge_service: ChallengeService):
        self.challenge_service = challenge_service

    def handle(self, command: GenerateChallengeCommand):
        return self.challenge_service.generate_challenge(command.difficulty, command.topic)