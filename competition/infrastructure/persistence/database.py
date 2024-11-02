from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Base declarativa para definir nuestros modelos de SQLAlchemy
Base = declarative_base()

load_dotenv()

# Datos de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)

# Crear la sesión
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    # Importar todos los modelos para asegurarse de que se crean las tablas
    from competition.infrastructure.persistence.models import CompetitionModel, ParticipantModel
    Base.metadata.create_all(bind=engine)