from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Datos de conexión a PostgreSQL
DATABASE_URL = "postgresql://avnadmin:AVNS_2MSqoAieULPkP2Kkg0J@cd-sd-skrak-34ad.b.aivencloud.com:28424/defaultdb"

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
