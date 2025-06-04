from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from app.models.todo import TodoStatus, TodoPriority


class TodoBase(BaseModel):
    """Base schema cho Todo"""
    title: str = Field(..., min_length=1, max_length=200, description="Tiêu đề của todo")
    description: Optional[str] = Field(None, description="Mô tả chi tiết của todo")
    status: Optional[TodoStatus] = Field(TodoStatus.PENDING, description="Trạng thái của todo")
    priority: Optional[TodoPriority] = Field(TodoPriority.MEDIUM, description="Mức độ ưu tiên")
    due_date: Optional[datetime] = Field(None, description="Ngày hết hạn")
    tags: Optional[List[str]] = Field(default_factory=list, description="Danh sách tags")


class TodoCreate(TodoBase):
    """Schema để tạo Todo mới"""
    pass


class TodoUpdate(BaseModel):
    """Schema để cập nhật Todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TodoStatusUpdate(BaseModel):
    """Schema để cập nhật chỉ trạng thái"""
    status: TodoStatus


class TodoResponse(TodoBase):
    """Schema cho response Todo"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TodoListResponse(BaseModel):
    """Schema cho danh sách todos"""
    todos: List[TodoResponse]
    total: int
    page: int
    size: int
    total_pages: int


class TodoStatsResponse(BaseModel):
    """Schema cho thống kê todos"""
    total_todos: int
    completed_todos: int
    pending_todos: int
    in_progress_todos: int
    overdue_todos: int
    high_priority_todos: int
    completion_rate: float
    todos_by_priority: Dict[str, int]
    todos_by_status: Dict[str, int]
    todos_by_tag: Dict[str, int]
    overdue_by_priority: Dict[str, int]


class TodoSearchParams(BaseModel):
    """Schema cho tham số tìm kiếm nâng cao"""
    query: str = Field(..., min_length=1, description="Từ khóa tìm kiếm")
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    tags: Optional[List[str]] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None


class TodoBulkCreate(BaseModel):
    """Schema cho tạo nhiều todos cùng lúc"""
    todos: List[TodoCreate] = Field(..., min_items=1, max_items=100)


class TodoBulkUpdate(BaseModel):
    """Schema cho cập nhật nhiều todos cùng lúc"""
    updates: Dict[str, TodoUpdate] = Field(
        ...,
        description="Dict với key là todo_id và value là thông tin cập nhật"
    ) 