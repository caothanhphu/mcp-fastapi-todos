# Thiết kế hệ thống Todos với MCP Server

## Tổng quan hệ thống

Hệ thống bao gồm 3 thành phần chính:
1. **Backend API (Python FastAPI)** - Quản lý dữ liệu todos
2. **MCP Server (Python)** - Cầu nối giữa Claude và Backend API
3. **Frontend UI (React)** - Giao diện web để quản lý todos

## Kiến trúc hệ thống

```
[Claude] ↔ [MCP Server] ↔ [Backend API] ↔ [Database]
                                ↕
                          [React Frontend]
```

## Phân tích yêu cầu và Tickets

### Phase 1: Backend API (Python FastAPI)

#### Ticket 1.1: Thiết lập dự án Backend
- **Mô tả**: Khởi tạo dự án FastAPI với cấu trúc thư mục chuẩn
- **Tasks**:
  - Tạo virtual environment và cài đặt dependencies
  - Thiết lập FastAPI application
  - Database dùng sqlite
  - Cấu hình CORS cho phép React frontend kết nối
  - Thiết lập logging và error handling
- **Dependencies**: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-multipart`

#### Ticket 1.2: Thiết kế Database Schema
- **Mô tả**: Thiết kế và tạo models cho todos
- **Models**:
  ```python
  # Todo model
  - id: UUID (Primary Key)
  - title: String (required)
  - description: Text (optional)
  - status: Enum (pending, in_progress, completed)
  - priority: Enum (low, medium, high)
  - due_date: DateTime (optional)
  - tags: List[String] (optional)
  - created_at: DateTime
  - updated_at: DateTime
  ```
- **Tasks**:
  - Tạo SQLAlchemy models
  - Thiết lập database migration với Alembic
  - Tạo sample data

#### Ticket 1.3: CRUD Operations API
- **Mô tả**: Implement các API endpoints cơ bản
- **Endpoints**:
  - `GET /todos` - Lấy danh sách todos (có filter, pagination)
  - `POST /todos` - Tạo todo mới
  - `GET /todos/{id}` - Lấy chi tiết todo
  - `PUT /todos/{id}` - Cập nhật todo
  - `DELETE /todos/{id}` - Xóa todo
  - `PATCH /todos/{id}/status` - Cập nhật trạng thái
- **Features**:
  - Validation với Pydantic
  - Error handling
  - Response formatting

#### Ticket 1.4: Advanced Features API
- **Mô tả**: Các tính năng nâng cao
- **Endpoints**:
  - `GET /todos/search` - Tìm kiếm todos theo từ khóa
  - `GET /todos/stats` - Thống kê todos
  - `POST /todos/bulk` - Tạo nhiều todos cùng lúc
  - `PUT /todos/bulk` - Cập nhật nhiều todos
- **Features**:
  - Full-text search
  - Filtering by tags, status, priority
  - Date range filtering

### Phase 2: MCP Server (Python)

#### Ticket 2.1: Thiết lập MCP Server Base
- **Mô tả**: Khởi tạo MCP server với cấu trúc cơ bản
- **Tasks**:
  - Cài đặt MCP SDK
  - Tạo server application
  - Thiết lập connection với Backend API
  - Implement health check
- **Dependencies**: `mcp`, `httpx`, `asyncio`

#### Ticket 2.2: Implement MCP Tools cho Todo Management
- **Mô tả**: Tạo các tools để Claude có thể quản lý todos
- **Tools**:
  ```python
  # Tool: create_todo
  - Input: title, description?, priority?, due_date?, tags?
  - Output: Created todo details
  
  # Tool: list_todos
  - Input: status?, priority?, tags?, limit?
  - Output: List of todos with pagination
  
  # Tool: update_todo
  - Input: todo_id, updates (title?, description?, status?, priority?)
  - Output: Updated todo details
  
  # Tool: delete_todo
  - Input: todo_id
  - Output: Success confirmation
  
  # Tool: search_todos
  - Input: query, filters?
  - Output: Matching todos
  ```

#### Ticket 2.3: Smart Todo Management Tools
- **Mô tả**: Các tools thông minh hơn để Claude có thể hiểu context
- **Tools**:
  ```python
  # Tool: complete_todos_by_description
  - Input: description_pattern
  - Output: List of completed todos
  
  # Tool: get_overdue_todos
  - Input: None
  - Output: List of overdue todos
  
  # Tool: prioritize_todos
  - Input: criteria (due_date, importance, etc.)
  - Output: Reordered todo list
  
  # Tool: get_todo_stats
  - Input: time_range?
  - Output: Statistics and insights
  ```

#### Ticket 2.4: Natural Language Processing
- **Mô tả**: Xử lý ngôn ngữ tự nhiên để tạo todos từ mô tả
- **Features**:
  - Parse due dates từ text ("tomorrow", "next week", "in 3 days")
  - Extract priority từ keywords ("urgent", "important", "low priority")
  - Auto-generate tags từ nội dung
  - Smart categorization

### Phase 3: React Frontend

#### Ticket 3.1: Thiết lập React Project
- **Mô tả**: Khởi tạo React app với các dependencies cần thiết
- **Tasks**:
  - Create React app với TypeScript
  - Cài đặt UI libraries (Tailwind CSS, Headless UI)
  - Thiết lập routing với React Router
  - Cấu hình API client (Axios)
- **Dependencies**: `react`, `typescript`, `tailwindcss`, `react-router-dom`, `axios`

#### Ticket 3.2: Core UI Components
- **Mô tả**: Tạo các component UI cơ bản
- **Components**:
  - `TodoList` - Hiển thị danh sách todos
  - `TodoItem` - Component cho từng todo
  - `TodoForm` - Form tạo/sửa todo
  - `FilterBar` - Thanh filter và search
  - `StatusBadge` - Badge hiển thị trạng thái
  - `PriorityIndicator` - Indicator mức độ ưu tiên

#### Ticket 3.3: Todo Management Features
- **Mô tả**: Implement các tính năng quản lý todos
- **Features**:
  - CRUD operations với API
  - Drag & drop để sắp xếp todos
  - Bulk actions (complete, delete multiple)
  - Real-time updates
  - Responsive design

#### Ticket 3.4: Advanced UI Features
- **Mô tả**: Các tính năng UI nâng cao
- **Features**:
  - Dashboard với charts và statistics
  - Calendar view cho due dates
  - Kanban board view
  - Dark/light theme toggle
  - Export todos (JSON, CSV)

### Phase 4: Integration & Testing

#### Ticket 4.1: End-to-end Integration
- **Mô tả**: Tích hợp toàn bộ hệ thống
- **Tasks**:
  - Thiết lập Docker containers cho tất cả services
  - Cấu hình reverse proxy (nginx)
  - Environment configuration
  - Database seeding

#### Ticket 4.2: Testing & Documentation
- **Mô tả**: Viết tests và documentation
- **Tasks**:
  - Unit tests cho Backend API
  - Integration tests cho MCP Server
  - E2E tests cho Frontend
  - API documentation với Swagger
  - MCP tools documentation
  - Deployment guide

## Demo Scenarios cho MCP Integration

### Scenario 1: Tạo Todo từ Chat
```
User: "Claude, tôi cần nhớ gọi điện cho khách hàng ABC vào ngày mai"
Claude: [Sử dụng create_todo tool]
Response: "Đã tạo todo: 'Gọi điện khách hàng ABC' với due date là ngày mai"
```

### Scenario 2: Quản lý Todo thông minh
```
User: "Những việc nào tôi cần làm gấp?"
Claude: [Sử dụng get_overdue_todos và list_todos với priority=high]
Response: "Bạn có 3 việc cần làm gấp: [danh sách todos]"
```

### Scenario 3: Phân tích và Insights
```
User: "Tôi hoàn thành bao nhiều việc tuần này?"
Claude: [Sử dụng get_todo_stats]
Response: "Tuần này bạn đã hoàn thành 12/15 việc, tăng 20% so với tuần trước"
```

## Tech Stack Summary

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL với SQLAlchemy ORM
- **Authentication**: JWT (optional)
- **Deployment**: Docker + Gunicorn

### MCP Server
- **Language**: Python 3.11+
- **Framework**: MCP SDK
- **HTTP Client**: httpx
- **Processing**: asyncio

### Frontend
- **Framework**: React 18 với TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Context API
- **Build Tool**: Vite

### DevOps
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: nginx
- **Database**: PostgreSQL
- **Deployment**: Cloud platform (AWS/GCP/Azure)

## Roadmap Timeline

- **Week 1-2**: Backend API (Tickets 1.1-1.4)
- **Week 3**: MCP Server (Tickets 2.1-2.2)
- **Week 4**: React Frontend (Tickets 3.1-3.2)
- **Week 5**: Advanced Features (Tickets 2.3-2.4, 3.3-3.4)
- **Week 6**: Integration & Testing (Tickets 4.1-4.2)
