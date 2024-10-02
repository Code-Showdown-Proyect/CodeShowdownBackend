from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ResponseModel(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'), nullable=False)
    answer = Column(Text, nullable=False)
    time_taken = Column(String(50), nullable=False)
    feedback = Column(Text, nullable=True)  # Almacena la retroalimentación generada
    is_correct = Column(Boolean, nullable=True)  # Indica si la respuesta es correcta
    score = Column(Integer, nullable=True)  # Puntaje basado en la evaluación

class FeedbackModel(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey('responses.id', ondelete='CASCADE'), nullable=False)
    detail = Column(Text, nullable=False)  # Retroalimentación proporcionada
    is_correct = Column(Boolean, nullable=False)  # Indica si la respuesta es correcta
    score = Column(Integer, nullable=False)  # Puntaje basado en la evaluación
    response = relationship("ResponseModel", back_populates="feedback")  # Relación con ResponseModel