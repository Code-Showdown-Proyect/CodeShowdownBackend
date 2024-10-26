import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Datos de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# Función para inicializar la base de datos
def init_db():
    from auth.infrastructure.persistence.models import Base
    Base.metadata.create_all(bind=engine)
