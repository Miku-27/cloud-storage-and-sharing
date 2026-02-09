from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import create_engine
from app.config import get_config

class Base(DeclarativeBase):
    pass

engine = create_engine(get_config().database_uri)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


