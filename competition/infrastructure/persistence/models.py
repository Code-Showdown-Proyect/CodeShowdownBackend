from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


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

    participants = relationship("ParticipantModel", back_populates="competition")


class ParticipantModel(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id', ondelete='CASCADE'), nullable=False)
    score = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)

    competition = relationship("CompetitionModel", back_populates="participants")

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String, nullable=False, unique=True)

class AnswerModel(Base):
    __tablename__ = 'submitted_answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'), nullable=False)
    answer = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    is_correct = Column(Boolean, nullable=True)
    feedback = Column(String, nullable=True)
    time_taken = Column(Numeric, nullable=False)

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