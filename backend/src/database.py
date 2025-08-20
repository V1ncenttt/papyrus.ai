import logging
import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# SQLite database URL for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scholarmind.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
    echo=False,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        # Import models to register them with Base

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ SQLite database tables created successfully")
        logger.info(f"📂 Database location: {DATABASE_URL}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def check_db_connection():
    """Check database connection health"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
