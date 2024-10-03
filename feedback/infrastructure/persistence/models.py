from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ResponseModel(Base):
    __tablename__ = 'submitted_answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'), nullable=False)
    answer = Column(Text, nullable=False)
    time_taken = Column(String(50), nullable=False)
    feedback = Column(Text, nullable=True)  # Almacena la retroalimentación generada
    is_correct = Column(Boolean, nullable=True)  # Indica si la respuesta es correcta

class FeedbackModel(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey('responses.id', ondelete='CASCADE'), nullable=False)
    detail = Column(Text, nullable=False)  # Retroalimentación proporcionada
    is_correct = Column(Boolean, nullable=False)  # Indica si la respuesta es correcta
    score = Column(Integer, nullable=False)  # Puntaje basado en la evaluación

class ParticipantModel(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id', ondelete='CASCADE'), nullable=False)
    score = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)

class ChallengeModel(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    competition_id = Column(Integer, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    output_example = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default='basic', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CompetitionModel(Base):
    __tablename__ = 'competitions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    number_of_exercises = Column(Integer, nullable=False)
    time_limit = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    access_code = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)