import json
from http.client import HTTPException

from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from starlette import status

from competition.application.services.competition_service import CompetitionService
from competition.infrastructure.persistence.database import SessionLocal
from typing import Optional

from competition.infrastructure.persistence.sqlalchemy_answer_repository import SQLAlchemyAnswerRepository
from competition.infrastructure.persistence.sqlalchemy_competition_repository import SQLAlchemyCompetitionRepository
from competition.infrastructure.persistence.sqlalchemy_participant_repository import SQLAlchemyParticipantRepository
from competition.infrastructure.real_time.socket_manager import ConnectionManager
from competition.security.authorization import get_current_user

router = APIRouter()
manager = ConnectionManager()


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
async def competition_websocket(websocket: WebSocket, competition_id: int, service: CompetitionService = Depends(get_competition_service)):
    global challenge_message
    token = websocket.headers.get("Authorization")
    try:
        # Validar el token y obtener el usuario actual
        current_user = get_current_user(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await websocket.accept()
    try:
        participant = service.participant_repository.find_by_user_and_competition(current_user, competition_id)
        print("Resultado de find_by_user_and_competition:", participant)
        if not participant:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            # Enviar desafío a todos los participantes cuando se inicie la competencia
            if data == "start_competition":
                competition = service.get_competition_by_id(competition_id)
                # Aquí se asume que el servicio genera los desafíos y devuelve el primero
                first_challenge = await service.generate_first_challenge(competition_id)
                challenge_message = {
                    "challenge_id": first_challenge["id"],
                    "title": first_challenge["title"],
                    "description": first_challenge["description"],
                    "time_limit": competition.time_limit
                }
                challenge_message_json = json.dumps(challenge_message)
                # Enviar el desafío a todos los participantes conectados a la competencia
                await manager.broadcast(challenge_message_json)

            # Recibir respuestas de los usuarios
            elif data.startswith("submit_answer"):
                # Extraer la información de la respuesta
                participant_id = service.participant_repository.find_by_user_and_competition(current_user, competition_id).id
                time_taken = 0
                exercise_id = challenge_message["challenge_id"]
                answer_data = data[len("submit_answer"):]

                try:
                    # Aquí se envía la respuesta al servicio para almacenarla
                    service.submit_answer(participant_id, competition_id, answer_data, time_taken, exercise_id)
                    # Enviar un mensaje de confirmación al usuario
                    await websocket.send_text("Respuesta enviada correctamente.")
                except Exception as e:
                    # Enviar un mensaje de error al usuario si algo falla
                    await websocket.send_text(f"Error al enviar la respuesta: {str(e)}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)

