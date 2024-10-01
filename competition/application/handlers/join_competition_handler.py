from competition.application.commands.join_competition_command import JoinCompetitionCommand
from competition.application.services.competition_service import CompetitionService

class JoinCompetitionHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: JoinCompetitionCommand):
        return self.service.join_competition(
            access_code=command.access_code,
            password=command.password,
            user_id= command.user_id
        )