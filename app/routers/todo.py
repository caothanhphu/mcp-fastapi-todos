from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, case
from datetime import datetime, timezone

from app.database import get_db
from app.models import Todo, TodoStatus, TodoPriority
from app.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
    TodoStatusUpdate,
    TodoStatsResponse,
    TodoSearchParams,
    TodoBulkCreate,
    TodoBulkUpdate
)

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


@router.get("", response_model=TodoListResponse)
async def list_todos(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng items mỗi trang"),
    status: Optional[TodoStatus] = Query(None, description="Lọc theo trạng thái"),
    priority: Optional[TodoPriority] = Query(None, description="Lọc theo độ ưu tiên"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo title hoặc description"),
    tag: Optional[str] = Query(None, description="Lọc theo tag"),
    due_before: Optional[datetime] = Query(None, description="Lọc các todo đến hạn trước ngày"),
    due_after: Optional[datetime] = Query(None, description="Lọc các todo đến hạn sau ngày")
):
    """Lấy danh sách todos với filter và pagination"""
    # Base query
    query = db.query(Todo)
    
    # Apply filters
    if status:
        query = query.filter(Todo.status == status)
    if priority:
        query = query.filter(Todo.priority == priority)
    if search:
        search_filter = or_(
            Todo.title.ilike(f"%{search}%"),
            Todo.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    if tag:
        query = query.filter(Todo.tags.contains([tag]))
    if due_before:
        query = query.filter(Todo.due_date <= due_before)
    if due_after:
        query = query.filter(Todo.due_date >= due_after)
    
    # Get total count for pagination
    total = query.count()
    total_pages = (total + size - 1) // size
    
    # Apply pagination
    query = query.order_by(Todo.created_at.desc())
    query = query.offset((page - 1) * size).limit(size)
    
    return TodoListResponse(
        todos=query.all(),
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    """Tạo todo mới"""
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    db: Session = Depends(get_db)
):
    """Lấy chi tiết một todo"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """Cập nhật toàn bộ thông tin của một todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.patch("/{todo_id}/status", response_model=TodoResponse)
async def update_todo_status(
    todo_id: str,
    status_update: TodoStatusUpdate,
    db: Session = Depends(get_db)
):
    """Cập nhật trạng thái của một todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.status = status_update.status
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str,
    db: Session = Depends(get_db)
):
    """Xóa một todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return None


@router.post("/search", response_model=TodoListResponse)
async def search_todos(
    search_params: TodoSearchParams,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng items mỗi trang")
):
    """Tìm kiếm nâng cao todos"""
    # Base query
    query = db.query(Todo)
    
    # Full text search
    search_filter = or_(
        Todo.title.ilike(f"%{search_params.query}%"),
        Todo.description.ilike(f"%{search_params.query}%")
    )
    query = query.filter(search_filter)
    
    # Apply additional filters
    if search_params.status:
        query = query.filter(Todo.status == search_params.status)
    if search_params.priority:
        query = query.filter(Todo.priority == search_params.priority)
    if search_params.tags:
        for tag in search_params.tags:
            query = query.filter(Todo.tags.contains([tag]))
    if search_params.due_before:
        query = query.filter(Todo.due_date <= search_params.due_before)
    if search_params.due_after:
        query = query.filter(Todo.due_date >= search_params.due_after)
    
    # Get total count for pagination
    total = query.count()
    total_pages = (total + size - 1) // size
    
    # Apply pagination
    query = query.order_by(Todo.created_at.desc())
    query = query.offset((page - 1) * size).limit(size)
    
    return TodoListResponse(
        todos=query.all(),
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )


@router.get("/stats", response_model=TodoStatsResponse)
async def get_todo_stats(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Ngày bắt đầu thống kê"),
    end_date: Optional[datetime] = Query(None, description="Ngày kết thúc thống kê")
):
    """Lấy thống kê về todos"""
    # Base query for todos, potentially filtered by date
    base_todos_query = db.query(Todo)
    if start_date:
        base_todos_query = base_todos_query.filter(Todo.created_at >= start_date)
    if end_date:
        base_todos_query = base_todos_query.filter(Todo.created_at <= end_date)
    
    # Get basic stats using the date-filtered query
    total_todos = base_todos_query.count()
    completed_todos = base_todos_query.filter(Todo.status == TodoStatus.COMPLETED).count()
    pending_todos = base_todos_query.filter(Todo.status == TodoStatus.PENDING).count()
    in_progress_todos = base_todos_query.filter(Todo.status == TodoStatus.IN_PROGRESS).count()
    high_priority_todos = base_todos_query.filter(Todo.priority == TodoPriority.HIGH).count()
    
    # Get overdue todos (excluding completed) using the date-filtered query
    now = datetime.now(timezone.utc)
    overdue_todos_query_base = base_todos_query.filter(
        Todo.due_date < now,
        Todo.status != TodoStatus.COMPLETED
    )
    overdue_todos = overdue_todos_query_base.count()
    
    # Calculate completion rate
    completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
    
    # Get todos by priority, applying date filters
    priority_query = db.query(
        Todo.priority,
        func.count(Todo.id).label("count")
    )
    if start_date:
        priority_query = priority_query.filter(Todo.created_at >= start_date)
    if end_date:
        priority_query = priority_query.filter(Todo.created_at <= end_date)
    priority_stats = priority_query.group_by(Todo.priority).all()
    todos_by_priority = {p.priority.value: p.count for p in priority_stats if p.priority}
    
    # Get todos by status, applying date filters
    status_query = db.query(
        Todo.status,
        func.count(Todo.id).label("count")
    )
    if start_date:
        status_query = status_query.filter(Todo.created_at >= start_date)
    if end_date:
        status_query = status_query.filter(Todo.created_at <= end_date)
    status_stats = status_query.group_by(Todo.status).all()
    todos_by_status = {s.status.value: s.count for s in status_stats if s.status}
    
    # Get todos by tag using the date-filtered query results
    tag_stats = {}
    all_filtered_todos = base_todos_query.all() # Use already filtered todos
    for todo in all_filtered_todos:
        for tag in (todo.tags or []):
            tag_stats[tag] = tag_stats.get(tag, 0) + 1
    
    # Get overdue todos by priority, applying date filters
    overdue_priority_query = db.query(
        Todo.priority,
        func.count(Todo.id).label("count")
    ).filter(
        Todo.due_date < now,
        Todo.status != TodoStatus.COMPLETED
    )
    if start_date:
        overdue_priority_query = overdue_priority_query.filter(Todo.created_at >= start_date)
    if end_date:
        overdue_priority_query = overdue_priority_query.filter(Todo.created_at <= end_date)
    
    overdue_priority_stats = overdue_priority_query.group_by(Todo.priority).all()
    overdue_by_priority = {p.priority.value: p.count for p in overdue_priority_stats if p.priority}
    
    return TodoStatsResponse(
        total_todos=total_todos,
        completed_todos=completed_todos,
        pending_todos=pending_todos,
        in_progress_todos=in_progress_todos,
        overdue_todos=overdue_todos,
        high_priority_todos=high_priority_todos,
        completion_rate=completion_rate,
        todos_by_priority=todos_by_priority,
        todos_by_status=todos_by_status,
        todos_by_tag=tag_stats,
        overdue_by_priority=overdue_by_priority
    )


@router.post("/bulk", response_model=List[TodoResponse], status_code=201)
async def create_bulk_todos(
    bulk_create: TodoBulkCreate,
    db: Session = Depends(get_db)
):
    """Tạo nhiều todos cùng lúc"""
    todos = []
    for todo_data in bulk_create.todos:
        db_todo = Todo(**todo_data.model_dump())
        todos.append(db_todo)
    
    db.add_all(todos)
    db.commit()
    
    # Refresh all todos to get their generated IDs
    for todo in todos:
        db.refresh(todo)
    
    return todos


@router.put("/bulk", response_model=List[TodoResponse])
async def update_bulk_todos(
    bulk_update: TodoBulkUpdate,
    db: Session = Depends(get_db)
):
    """Cập nhật nhiều todos cùng lúc"""
    # Get all todos that need to be updated
    todo_ids = list(bulk_update.updates.keys())
    todos = db.query(Todo).filter(Todo.id.in_(todo_ids)).all()
    
    # Create a map of id to todo for easy access
    todo_map = {todo.id: todo for todo in todos}
    
    # Check if all todos exist
    missing_ids = set(todo_ids) - set(todo_map.keys())
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Todos not found: {missing_ids}"
        )
    
    # Update each todo
    for todo_id, update_data in bulk_update.updates.items():
        todo = todo_map[todo_id]
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(todo, field, value)
    
    db.commit()
    
    # Refresh all todos to get their updated values
    for todo in todos:
        db.refresh(todo)
    
    return todos 