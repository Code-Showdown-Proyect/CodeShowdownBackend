from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


Base = declarative_base()

class UserStatisticsModel(Base):
    __tablename__ = 'users_statistics'

    # challenge stats
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    competitions_completed = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    average_time_per_competition = Column(Float, default=0.0)
    average_score_per_competition = Column(Float, default=0.0)

    #challenge stats
    average_time_per_challenge = Column(Float, default=0.0)
    best_score = Column(Integer, default=0)
    challenge_completed_count = Column(Integer, default=0)

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

class UserProfileModel(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    description = Column(String, nullable=True)