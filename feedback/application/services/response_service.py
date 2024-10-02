# response_service.py
from feedback.domain.entities.response import Response
from feedback.domain.repositories.response_repository import ResponseRepository
from feedback.domain.repositories.feedback_repository import FeedbackRepository

class ResponseService:
    def __init__(self, response_repository: ResponseRepository, feedback_repository: FeedbackRepository):
        self.response_repository = response_repository
        self.feedback_repository = feedback_repository

    def create_response(self, response: Response):
        return self.response_repository.create_response(response)

    def update_response_with_feedback(self, response_id: int, feedback_content: str, is_correct: bool, score: int):
        self.response_repository.update_response_with_feedback(response_id, feedback_content, is_correct, score)

    def generate_feedback(self, response_id: int):
        # Lógica para generar feedback usando la API de ChatGPT
        # Posteriormente se llama a `update_response_with_feedback`
        pass