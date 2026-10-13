import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.models.product import Base

engine = None
SessionLocal = None
is_postgres_active = False

def init_db():
    global engine, SessionLocal, is_postgres_active
    
    # Try PostgreSQL if URL is provided
    db_url = settings.DATABASE_URL
    if db_url and "postgresql" in db_url:
        try:
            temp_engine = create_engine(db_url, connect_args={"connect_timeout": 3})
            # Test connection
            with temp_engine.connect() as conn:
                pass
            engine = temp_engine
            is_postgres_active = True
            logger.info("Successfully connected to PostgreSQL database.")
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed ({e}). Falling back to local SQLite/sample mode.")
            is_postgres_active = False
            
    if not is_postgres_active:
        # Fallback to local SQLite database in app directory
        sqlite_path = os.path.join(os.path.dirname(__file__), "ava_local.db")
        engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
        logger.info(f"Using SQLite database engine at {sqlite_path}")

    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

init_db()

def get_db():
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
