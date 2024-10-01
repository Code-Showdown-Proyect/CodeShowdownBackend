from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from competition.application.services.competition_service import CompetitionService
from competition.infrastructure.persistence.database import SessionLocal
from typing import Optional

from competition.infrastructure.persistence.sqlalchemy_competition_repository import SQLAlchemyCompetitionRepository
from competition.infrastructure.persistence.sqlalchemy_participant_repository import SQLAlchemyParticipantRepository
from competition.infrastructure.real_time.socket_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


# Dependency to get the competition service
def get_competition_service():
    db = SessionLocal()
    try:
        competition_repository = SQLAlchemyCompetitionRepository(db)
        participant_repository = SQLAlchemyParticipantRepository(db)
        return CompetitionService(competition_repository, participant_repository)
    finally:
        db.close()


@router.websocket("/ws/competition/{competition_id}")
async def competition_websocket(websocket: WebSocket, competition_id: int,
                                service: CompetitionService = Depends(get_competition_service)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # Enviar desafío a todos los participantes cuando se inicie la competencia
            if data == "start_competition":
                competition = service.get_competition_by_id(competition_id)

                # Aquí se asume que el servicio genera los desafíos y devuelve el primero
                first_challenge = service.generate_first_challenge(competition_id)
                challenge_message = {
                    "challenge_id": first_challenge.id,
                    "title": first_challenge.title,
                    "description": first_challenge.description,
                    "time_limit": competition.time_limit
                }

                # Enviar el desafío a todos los participantes conectados a la competencia
                await manager.broadcast(challenge_message)

            # Recibir respuestas de los usuarios
            elif data.startswith("submit_answer"):
                # Extraer la información de la respuesta
                participant_id = websocket.headers.get('participant-id')
                answer_data = data[len("submit_answer "):]

                # Aquí se envía la respuesta al servicio para almacenarla
                service.submit_answer(competition_id, participant_id, answer_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)