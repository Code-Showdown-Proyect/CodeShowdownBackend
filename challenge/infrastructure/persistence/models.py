from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from challenge.infrastructure.database import Base
from datetime import datetime

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