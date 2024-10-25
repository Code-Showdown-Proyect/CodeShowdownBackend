from feedback.domain.repositories.feedback_repository import FeedbackRepository
from feedback.domain.repositories.response_repository import ResponseRepository
from feedback.infrastructure.external.chatgpt_client import ChatGPTClient
from feedback.domain.entities.feedback import Feedback
from typing import List


class FeedbackService:
    def __init__(self, response_repository: ResponseRepository, feedback_repository: FeedbackRepository):
        self.response_repository = response_repository
        self.feedback_repository = feedback_repository
        self.chatgpt_client = ChatGPTClient()


    def generate_feedback(self, participant_id: int) -> List[Feedback]:
        response = self.response_repository.find_by_id(participant_id)

        if not response:
            raise ValueError("Response not found")
        feedback_details = []  # Para almacenar la retroalimentación generada
        scores = []  # Para almacenar los puntajes
        for resp in response:
            if not resp.answer.strip():
                feedback_detail = {"feedback": "No se proporcionó ninguna respuesta. Recuerda que participar y enviar tu solución es importante para recibir retroalimentación."}
                is_correct = False
                score = 0
            else:
                question = self.response_repository.find_question_by_id(resp.challenge_id)
                feedback_detail = self.chatgpt_client.generate_feedback(resp.answer,question.description)
                is_correct = self._evaluate_correctness(feedback_detail["conclusion"])
                score = feedback_detail["score"]

            # Actualizar la respuesta con la retroalimentación
            self.response_repository.update_response_with_feedback(participant_id, feedback_detail["feedback"], is_correct)
            # Crear la entidad Feedback
            feedback = Feedback(
                id=None,
                response_id=resp.id,
                detail=feedback_detail["feedback"],
                is_correct=is_correct,
                score=score
            )
            feedback_details.append(feedback)
            scores.append(score)
        self.response_repository.update_score(participant_id, scores)
        return feedback_details

    def _evaluate_correctness(self, feedback_detail: str) -> bool:
        correctness_indicators = ["correcto", "bien hecho", "solución válida", "resolución correcta","Problema resuelto correctamente"]
        return any(indicator in feedback_detail.lower() for indicator in correctness_indicators)


