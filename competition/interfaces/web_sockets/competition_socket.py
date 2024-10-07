import json
from collections import defaultdict
from http.client import HTTPException

import httpx
from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from starlette import status

from competition.application.services.competition_service import CompetitionService
from competition.infrastructure.persistence.database import SessionLocal
from typing import Optional

from competition.infrastructure.persistence.sqlalchemy_answer_repository import SQLAlchemyAnswerRepository
from competition.infrastructure.persistence.sqlalchemy_competition_repository import SQLAlchemyCompetitionRepository
from competition.infrastructure.persistence.sqlalchemy_participant_repository import SQLAlchemyParticipantRepository
from competition.infrastructure.real_time.socket_manager import ConnectionManager
from competition.security.authorization import get_current_user, get_current_username

router = APIRouter()
manager = ConnectionManager()
responses_count = defaultdict(int)  # Cantidad de respuestas recibidas por desafío para cada competencia
participant_progress = defaultdict(dict)  # Progreso de cada participante

completed_participants = set()  # Conjunto de participantes que han completado la competencia
FEEDBACK_SERVICE_URL = "http://127.0.0.1:8000/feedback/analyze-response"

# Dependency to get the competition service
def get_competition_service():
    db = SessionLocal()
    try:
        competition_repository = SQLAlchemyCompetitionRepository(db)
        participant_repository = SQLAlchemyParticipantRepository(db)
        answer_repository = SQLAlchemyAnswerRepository(db)
        return CompetitionService(competition_repository, participant_repository, answer_repository)
    finally:
        db.close()


@router.websocket("/competition/{competition_id}")
async def competition_websocket(websocket: WebSocket, competition_id: int,
                                service: CompetitionService = Depends(get_competition_service)):
    token = websocket.headers.get("Authorization")
    try:
        # Validar el token y obtener el usuario actual
        current_user = get_current_user(token)
        current_username = get_current_username(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    try:
        participant = service.participant_repository.find_by_user_and_competition(current_user, competition_id)
        if not participant:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await manager.connect(websocket)

        # Inicializar el progreso del participante si no está registrado
        if participant.id not in participant_progress[competition_id]:
            competition = service.get_competition_by_id(competition_id)
            challenges_list = service.competition_repository.get_challenges_by_competition_id(competition_id)
            participant_progress[competition_id][participant.id] = {
                "challenges": challenges_list,  # Lista de desafíos de la competencia
                "current_index": 0,  # Índice del desafío actual
                "completed_challenges": 0  # Número de desafíos completados por el participante
            }

        while True:
            data = await websocket.receive_text()

            # Enviar el primer desafío a todos los participantes al iniciar la competencia
            if data == "start_competition":
                # Obtener el primer desafío
                first_challenge = participant_progress[competition_id][participant.id]["challenges"][0]
                challenge_message = {
                    "challenge_id": first_challenge.id,
                    "title": first_challenge.title,
                    "description": first_challenge.description,
                    "difficulty": first_challenge.difficulty,
                    "output_example": first_challenge.output_example,
                    "time_limit": competition.time_limit
                }
                # Enviar el primer desafío a todos los participantes conectados
                await manager.broadcast(json.dumps(challenge_message))

            elif data.startswith("submit_answer"):
                # Extraer la información de la respuesta
                answer_data = data[len("submit_answer"):]
                participant_data = participant_progress[competition_id][participant.id]
                current_index = participant_data["current_index"]
                current_challenge = participant_data["challenges"][current_index]

                try:
                    # Aquí se envía la respuesta al servicio para almacenarla
                    service.submit_answer(participant.id, competition_id, answer_data, 0, current_challenge.id)
                    participant_data["completed_challenges"] += 1

                    # Incrementar el contador de respuestas completadas para el desafío actual
                    responses_count[(competition_id, current_index)] += 1

                    # Verificar si todos los participantes han completado el desafío actual
                    total_participants = service.participant_repository.count_by_competition(competition_id)
                    if responses_count[(competition_id, current_index)] >= total_participants:
                        # Todos los participantes han completado el desafío actual, avanzar al siguiente
                        for p_id in participant_progress[competition_id]:
                            participant_progress[competition_id][p_id]["current_index"] += 1

                        # Verificar si hay un próximo desafío
                        next_index = participant_progress[competition_id][participant.id]["current_index"]
                        if next_index < len(participant_data["challenges"]):
                            next_challenge = participant_data["challenges"][next_index]
                            challenge_message = {
                                "challenge_id": next_challenge.id,
                                "title": next_challenge.title,
                                "description": next_challenge.description,
                                "difficulty": next_challenge.difficulty,
                                "output_example": next_challenge.output_example
                            }
                            # Enviar el siguiente desafío a todos los participantes conectados
                            await manager.broadcast(json.dumps(challenge_message))
                        else:
                            # Si todos los desafíos han sido completados
                            await manager.broadcast(json.dumps({"action": "all_participants_done"}))
                            await analyze_responses_for_all_participants(competition_id, websocket)
                            await analyze_feedback_for_all_participants(competition_id, current_user, websocket, service)
                    else:
                        # Notificar al participante que debe esperar a que los demás terminen
                        await websocket.send_text(
                            "Esperando a que todos los participantes completen el desafío actual.")

                except Exception as e:
                    # Enviar un mensaje de error al usuario si algo falla
                    await websocket.send_text(f"Error al enviar la respuesta: {str(e)}")

            elif data.startswith("chat_message"):
                message_content = data[len("chat_message"):]
                chat_message = {
                    "user": current_username,
                    "message": message_content
                }
                await manager.broadcast(json.dumps(chat_message))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def analyze_responses_for_all_participants(competition_id: int, websocket: WebSocket):

    participants = participant_progress[competition_id].keys()

    for participant_id in participants:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    FEEDBACK_SERVICE_URL,
                    json={"participant_id": participant_id}
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            await websocket.send_text(f"Error al analizar las respuestas: {e.response.status_code} {e.response.text}")
        except Exception as e:
            import traceback
            traceback_message = traceback.format_exc()  # Obtener la traza del error
            await websocket.send_text(
                f"Error desconocido al analizar las respuestas: {str(e)}. Traceback: {traceback_message}")


async def analyze_feedback_for_all_participants(competition_id: int, current_user: int, websocket: WebSocket, service: CompetitionService = Depends(get_competition_service)):

    participants = participant_progress[competition_id].keys()
    feedback_messages = []

    # Recopilar los feedbacks de todos los participantes desde la base de datos
    for participant_id in participants:
        try:
            feedbacks = service.competition_repository.get_feedbacks_by_participant(participant_id)
            challenges_list = service.competition_repository.get_challenges_by_competition_id(competition_id)

            # Relacionar feedbacks con sus desafíos correspondientes
            feedback_message = {
                "participant_id": participant_id,
                "feedbacks": []
            }
            for challenge in challenges_list:
                for feedback in feedbacks:
                    if feedback.challenge_id == challenge.id:
                        feedback_message["feedbacks"].append({
                            "challenge_title": challenge.title,
                            "feedback": feedback.feedback,
                            "score": service.participant_repository.find_by_user_and_competition(current_user, competition_id).score
                        })
                        break

            feedback_messages.append(feedback_message)

        except Exception as e:
            await websocket.send_text(f"Error al recopilar feedbacks: {str(e)}")

    # Enviar los mensajes de feedback a todos los participantes conectados
    for feedback_message in feedback_messages:
        await manager.broadcast(json.dumps(feedback_message))