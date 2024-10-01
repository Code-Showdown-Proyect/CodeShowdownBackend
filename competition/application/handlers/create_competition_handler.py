from competition.application.commands.create_competition_command import CreateCompetitionCommand
from competition.application.services.competition_service import CompetitionService

class CreateCompetitionHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: CreateCompetitionCommand):
        return self.service.create_competition(
            name=command.name,
            number_of_exercises=command.number_of_exercises,
            time_limit=command.time_limit,
            password=command.password
        )