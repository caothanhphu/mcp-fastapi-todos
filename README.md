# FastAPI Backend Project

Dự án Backend sử dụng FastAPI với SQLite database và cấu hình CORS cho React frontend.

## Cấu trúc thư mục

```
app/
├── __init__.py          # Package marker
├── main.py              # FastAPI application chính
├── config.py            # Cấu hình ứng dụng
├── database.py          # Cấu hình database
├── models/              # SQLAlchemy models
│   └── __init__.py
├── schemas/             # Pydantic schemas
│   └── __init__.py
├── routers/             # API routers
│   └── __init__.py
└── services/            # Business logic
    └── __init__.py
```

## Cài đặt

### 1. Tạo virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

```bash
# Copy file cấu hình mẫu
copy env.example .env

# Chỉnh sửa file .env theo nhu cầu
```

### 4. Chạy ứng dụng

```bash
# Development mode với auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Tính năng

- ✅ FastAPI với automatic API documentation
- ✅ SQLite database với SQLAlchemy ORM
- ✅ CORS middleware cho React frontend
- ✅ Logging và error handling
- ✅ Pydantic models cho data validation
- ✅ Cấu trúc project theo best practices
- ✅ Environment configuration

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Database

Ứng dụng sử dụng SQLite database với:
- Async support thông qua `aiosqlite`
- SQLAlchemy ORM cho database operations
- Automatic table creation
- Database connection pooling

## CORS Configuration

CORS được cấu hình để cho phép kết nối từ:
- `http://localhost:3000` (React CRA)
- `http://localhost:5173` (Vite)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

## Logging

- Log level: INFO
- Output: Console và file `app.log`
- Format: Timestamp, logger name, level, message

## Development

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Production Deployment

1. Set environment variables
2. Change SECRET_KEY in production
3. Set DEBUG=False
4. Use production WSGI server như Gunicorn
5. Configure reverse proxy (Nginx)

## Dependencies

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - SQL toolkit và ORM
- `pydantic` - Data validation
- `python-multipart` - Form data parsing
- `databases` - Async database support
- `aiosqlite` - Async SQLite driver 