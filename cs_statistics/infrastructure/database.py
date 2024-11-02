import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Datos de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de conexión para PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Crear la clase base para los modelos ORM
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)