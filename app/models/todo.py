from sqlalchemy import Column, String, Text, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
import uuid
from app.database import Base


class TodoStatus(enum.Enum):
    """Enum cho trạng thái của Todo"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(enum.Enum):
    """Enum cho mức độ ưu tiên của Todo"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(Base):
    """Model cho Todo"""
    __tablename__ = "todos"

    # UUID primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # Basic info
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Status and priority
    status = Column(Enum(TodoStatus), default=TodoStatus.PENDING, nullable=False, index=True)
    priority = Column(Enum(TodoPriority), default=TodoPriority.MEDIUM, nullable=False, index=True)
    
    # Due date
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    
    # Tags (stored as JSON for SQLite compatibility)
    tags = Column(JSON, nullable=True, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title={self.title}, status={self.status.value})>" 