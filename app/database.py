from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# SQLite database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("+aiosqlite", "")
DATABASE_URL = settings.DATABASE_URL

# Tạo engine cho SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Cần thiết cho SQLite
    echo=settings.DEBUG  # Log SQL queries khi debug
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo base class cho models
Base = declarative_base()

# Tạo database instance cho async operations
database = Database(DATABASE_URL)

# Metadata cho async database operations
metadata = MetaData()


async def init_db():
    """Khởi tạo database"""
    try:
        await database.connect()
        logger.info("Database connected successfully")
        
        # Tạo các bảng
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def close_db():
    """Đóng kết nối database"""
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Error closing database: {e}")


def get_db():
    """Dependency để lấy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependency để lấy async database connection"""
    return database 