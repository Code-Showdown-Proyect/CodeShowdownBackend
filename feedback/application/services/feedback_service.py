from feedback.domain.repositories.feedback_repository import FeedbackRepository
from feedback.domain.repositories.response_repository import ResponseRepository
from feedback.infrastructure.external.chatgpt_client import ChatGPTClient
from feedback.domain.entities.feedback import Feedback
from typing import Optional

class FeedbackService:
    def __init__(self, response_repository: ResponseRepository, feedback_repository: FeedbackRepository):
        self.response_repository = response_repository
        self.feedback_repository = feedback_repository
        self.chatgpt_client = ChatGPTClient()  # Cliente para interactuar con la API de ChatGPT


    def generate_feedback(self, response_id: int) -> Optional[Feedback]:
        # Encontrar la respuesta por su ID
        response = self.response_repository.find_by_id(response_id)
        if not response:
            raise ValueError("Response not found")

        # Si la respuesta está vacía, generar feedback indicando que no hubo respuesta
        if not response.answer.strip():
            feedback_detail = "No se proporcionó ninguna respuesta. Recuerda que participar y enviar tu solución es importante para recibir retroalimentación."
            is_correct = False
            score = 0
        else:
            # Usar ChatGPT para generar la retroalimentación
            feedback_detail = self.chatgpt_client.generate_feedback(response.answer)

            # Evaluar la corrección de la respuesta y calcular el puntaje
            is_correct = self._evaluate_correctness(feedback_detail)
            score = self._calculate_score(feedback_detail)

        # Crear la entidad Feedback
        feedback = Feedback(
            id=None,
            response_id=response.id,
            detail=feedback_detail,
            is_correct=is_correct,
            score=score
        )

        # Guardar la retroalimentación en la base de datos
        self.feedback_repository.save(feedback)

        # Actualizar la respuesta con la retroalimentación
        self.response_repository.update_response_with_feedback(response.id, feedback.detail, feedback.is_correct, feedback.score)

        return feedback

    def _evaluate_correctness(self, feedback_detail: str) -> bool:
        """
        Lógica para evaluar si la respuesta es correcta basándose en el contenido del feedback.
        """
        # Evaluar si la respuesta fue correcta basándose en la retroalimentación
        correctness_indicators = ["correcto", "bien hecho", "solución válida", "resolución correcta"]
        return any(indicator in feedback_detail.lower() for indicator in correctness_indicators)

    def _calculate_score(self, feedback_detail: str) -> int:
        """
        Lógica para calcular el puntaje de la respuesta basándose en el feedback.
        """
        # Puntaje de 100 si la respuesta es correcta, caso contrario 50, o ajustar según reglas
        return 100 if self._evaluate_correctness(feedback_detail) else 50