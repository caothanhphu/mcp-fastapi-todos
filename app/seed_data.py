"""
Script để tạo sample data cho development
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database import SQLALCHEMY_DATABASE_URL
from app.models import Todo, TodoStatus, TodoPriority


# Sample todos data
SAMPLE_TODOS = [
    {
        "title": "Hoàn thành báo cáo tháng",
        "description": "Viết báo cáo tổng kết công việc tháng này và gửi cho manager",
        "status": TodoStatus.IN_PROGRESS,
        "priority": TodoPriority.HIGH,
        "due_date": datetime.now() + timedelta(days=2),
        "tags": ["work", "report", "important"]
    },
    {
        "title": "Mua sắm cuối tuần",
        "description": "Mua thực phẩm và đồ dùng gia đình cho tuần mới",
        "status": TodoStatus.PENDING,
        "priority": TodoPriority.MEDIUM,
        "due_date": datetime.now() + timedelta(days=3),
        "tags": ["personal", "shopping", "family"]
    },
    {
        "title": "Học Python FastAPI",
        "description": "Hoàn thành khóa học FastAPI trên online platform",
        "status": TodoStatus.IN_PROGRESS,
        "priority": TodoPriority.MEDIUM,
        "due_date": datetime.now() + timedelta(days=7),
        "tags": ["learning", "programming", "python"]
    },
    {
        "title": "Đặt lịch khám răng",
        "description": "Gọi điện đặt lịch khám răng định kỳ",
        "status": TodoStatus.PENDING,
        "priority": TodoPriority.LOW,
        "due_date": datetime.now() + timedelta(days=5),
        "tags": ["health", "personal", "appointment"]
    },
    {
        "title": "Backup dữ liệu laptop",
        "description": "Sao lưu toàn bộ dữ liệu quan trọng lên cloud storage",
        "status": TodoStatus.PENDING,
        "priority": TodoPriority.HIGH,
        "due_date": datetime.now() + timedelta(days=1),
        "tags": ["tech", "backup", "important"]
    },
    {
        "title": "Đọc sách về AI",
        "description": "Đọc xong cuốn sách 'Artificial Intelligence: A Modern Approach'",
        "status": TodoStatus.IN_PROGRESS,
        "priority": TodoPriority.MEDIUM,
        "due_date": datetime.now() + timedelta(days=14),
        "tags": ["reading", "ai", "learning"]
    },
    {
        "title": "Tập thể dục",
        "description": "Tập gym 3 lần trong tuần",
        "status": TodoStatus.COMPLETED,
        "priority": TodoPriority.MEDIUM,
        "due_date": datetime.now() - timedelta(days=1),
        "tags": ["health", "fitness", "personal"]
    },
    {
        "title": "Chuẩn bị presentation",
        "description": "Làm slide cho buổi presentation về dự án mới",
        "status": TodoStatus.PENDING,
        "priority": TodoPriority.HIGH,
        "due_date": datetime.now() + timedelta(hours=12),
        "tags": ["work", "presentation", "urgent"]
    },
    {
        "title": "Học tiếng Anh",
        "description": "Hoàn thành bài học Unit 10 trong sách tiếng Anh",
        "status": TodoStatus.PENDING,
        "priority": TodoPriority.LOW,
        "due_date": datetime.now() + timedelta(days=10),
        "tags": ["learning", "english", "language"]
    },
    {
        "title": "Sửa chữa xe máy",
        "description": "Đưa xe máy đi bảo dưỡng định kỳ",
        "status": TodoStatus.COMPLETED,
        "priority": TodoPriority.MEDIUM,
        "due_date": datetime.now() - timedelta(days=3),
        "tags": ["vehicle", "maintenance", "personal"]
    }
]


def create_sample_todos():
    """Tạo sample todos trong database"""
    # Create engine and session
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        # Check if todos already exist
        existing_count = db.query(Todo).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} todos. Skipping seed.")
            return
        
        # Create sample todos
        todos = []
        for todo_data in SAMPLE_TODOS:
            todo = Todo(**todo_data)
            todos.append(todo)
        
        # Add all todos to database
        db.add_all(todos)
        db.commit()
        
        print(f"Successfully created {len(todos)} sample todos!")
        
        # Print summary
        for status in TodoStatus:
            count = db.query(Todo).filter(Todo.status == status).count()
            print(f"- {status.value}: {count} todos")
            
    except Exception as e:
        print(f"Error creating sample todos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_todos() 