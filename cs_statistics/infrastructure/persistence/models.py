from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from cs_statistics.infrastructure.database import Base


class CompetitionStatisticsModel(Base):
    __tablename__ = 'competition_statistics'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    competitions_completed = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    average_time_per_competition = Column(Float, default=0.0)
    average_score_per_competition = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChallengeStatisticsModel(Base):
    __tablename__ = 'challenge_statistics'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'), nullable=False)
    average_time_per_challenge = Column(Float, default=0.0)
    best_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class FeedbackImprovementStatisticsModel(Base):
    __tablename__ = 'feedback_improvement_statistics'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    feedback_applied_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

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

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default='basic', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

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

