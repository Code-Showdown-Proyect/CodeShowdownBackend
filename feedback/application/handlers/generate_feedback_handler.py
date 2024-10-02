from feedback.application.commands.generate_feedback_command import GenerateFeedbackCommand
from feedback.application.services.feedback_service import FeedbackService


class GenerateFeedbackHandler:
    def __init__(self, feedback_service: FeedbackService):
        self.feedback_service = feedback_service

    def handle(self, command: GenerateFeedbackCommand) -> None:
        self.feedback_service.generate_feedback_for_response(command.response_id)