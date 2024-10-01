from datetime import datetime
from typing import List, Optional

class Competition:
    def __init__(self, id: int, name: str, number_of_exercises: int, time_limit: int, created_at: datetime, creator_id: int, status: str = 'pending', access_code: str = None, password: Optional[str] = None):
        self.id = id
        self.name = name
        self.number_of_exercises = number_of_exercises
        self.time_limit = time_limit  # en minutos
        self.created_at = created_at
        self.status = status
        self.access_code = access_code
        self.password = password  # Contraseña opcional para la sala
        self.creator_id = creator_id  # ID del usuario creador de la competencia
        self.participants = []  # Lista de participantes en la competencia
        self.exercises = []  # Lista de ejercicios asignados a la competencia

    def set_creator(self, creator_id: int):
        self.creator_id = creator_id

    def add_participant(self, participant):
        self.participants.append(participant)

    def remove_participant(self, participant_id: int):
        self.participants = [p for p in self.participants if p.id != participant_id]

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def verify_access_code(self, access_code: str) -> bool:
        return self.access_code == access_code

    def verify_password(self, password: Optional[str]) -> bool:
        if self.password is None:
            return True  # Sala pública, no requiere contraseña
        return self.password == password

    def kick_participant(self, participant_id: int, user_id: int) -> bool:
        
        if user_id != self.creator_id:
            raise PermissionError("Only the creator of the competition can kick participants.")
        for participant in self.participants:
            if participant.id == participant_id:
                self.remove_participant(participant_id)
                return True
        return False

    def __repr__(self):
        return f"Competition(id={self.id}, name='{self.name}', number_of_exercises={self.number_of_exercises}, status='{self.status}', access_code='{self.access_code}')"