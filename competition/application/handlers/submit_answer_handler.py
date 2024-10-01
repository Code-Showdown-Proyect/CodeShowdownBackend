from competition.application.commands.submit_answer_command import SubmitAnswerCommand
from competition.application.services.competition_service import CompetitionService

class SubmitAnswerHandler:
    def __init__(self, service: CompetitionService):
        self.service = service

    def handle(self, command: SubmitAnswerCommand):
        # Aquí podemos agregar lógica para evaluar la respuesta.
        pass  # La lógica para evaluar la respuesta y actualizar el score