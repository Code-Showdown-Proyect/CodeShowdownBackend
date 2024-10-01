from competition.application.commands.delete_competition_command import DeleteCompetitionCommand
from competition.application.services.competition_service import CompetitionService

class DeleteCompetitionHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: DeleteCompetitionCommand):
        return self.service.delete_competition(competition_id=command.competition_id, creator_id=command.creator_id)