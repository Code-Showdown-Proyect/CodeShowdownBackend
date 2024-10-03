from feedback.application.commands.analyze_response_command import AnalyzeResponseCommand
from feedback.application.services.feedback_service import FeedbackService

class AnalyzeResponseHandler:
    def __init__(self, feedback_service: FeedbackService):
        self.feedback_service = feedback_service

    def handle(self, command: AnalyzeResponseCommand):
        # Llama al servicio para generar la retroalimentación
        feedback = self.feedback_service.generate_feedback(command.participant_id)
        return feedback