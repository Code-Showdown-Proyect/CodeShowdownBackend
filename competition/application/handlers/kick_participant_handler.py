from competition.application.commands.kick_participant_command import KickParticipantCommand
from competition.application.services.competition_service import CompetitionService


class KickParticipantHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: KickParticipantCommand):
        return self.service.kick_participant(
            competition_id=command.competition_id,
            creator_id=command.creator_id,
            participant_id=command.participant_id
        )