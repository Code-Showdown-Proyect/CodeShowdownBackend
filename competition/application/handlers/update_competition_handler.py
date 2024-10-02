from competition.application.commands.update_competition_command import UpdateCompetitionCommand
from competition.application.services.competition_service import CompetitionService



class UpdateCompetitionHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: UpdateCompetitionCommand):
        return self.service.update_competition(
            creator_id= command.creator_id,
            time_limit= command.time_limit,
            competition_id= command.competition_id,
            name= command.name,
            password= command.password,
            number_of_exercises= command.number_of_exercises
        )