import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://avnadmin:AVNS_2MSqoAieULPkP2Kkg0J@cd-sd-skrak-34ad.b.aivencloud.com:28424/defaultdb")

# Crear el motor de conexión para PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Crear la clase base para los modelos ORM
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)