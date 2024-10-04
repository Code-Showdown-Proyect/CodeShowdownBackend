from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfileModel(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return (f"UserProfileModel(id={self.id}, user_id={self.user_id}, "
                f"first_name={self.first_name}, last_name={self.last_name}, "
                f"profile_picture_url={self.profile_picture_url}, description={self.description}")
