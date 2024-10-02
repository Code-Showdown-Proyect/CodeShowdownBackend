from competition.application.commands.update_status_command import UpdateStatusCommand
from competition.application.services.competition_service import CompetitionService


class UpdateStatusHandler:
    def __init__(self, CompetitionService):
        self.service = CompetitionService

    def handle(self, command: UpdateStatusCommand):
        return self.service.update_status(
            competition_id=command.competition_id,
            status=command.status
        )