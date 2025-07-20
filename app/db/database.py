from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import Settings


engine = create_engine(Settings().DATABASE_URL, echo=True)


Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
