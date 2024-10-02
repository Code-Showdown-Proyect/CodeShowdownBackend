from competition.application.commands.submit_answer_command import SubmitAnswerCommand
from competition.application.services.competition_service import CompetitionService

class SubmitAnswerHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: SubmitAnswerCommand):
        # Aquí podemos agregar lógica para evaluar la respuesta.
        return self.service.submit_answer(
            participant_id=command.participant_id,
            competition_id=command.competition_id,
            answer=command.answer,
            exercise_id=command.exercise_id,
            time_taken=command.time_taken

        )
