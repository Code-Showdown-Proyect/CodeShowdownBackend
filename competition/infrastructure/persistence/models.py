from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_code = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)

    participants = relationship("ParticipantModel", back_populates="competition")


class ParticipantModel(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)
    score = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)

    competition = relationship("CompetitionModel", back_populates="participants")