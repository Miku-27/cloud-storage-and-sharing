from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import create_engine
from app.config import dev_setting

class Base(DeclarativeBase):
    pass

engine = create_engine(dev_setting.database_uri)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


