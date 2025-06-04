from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from contextlib import asynccontextmanager

from app.database import init_db
from app.config import settings
from app.routers import todo_router


# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager cho FastAPI app"""
    logger.info("Starting up application...")
    await init_db()
    yield
    logger.info("Shutting down application...")


# Khởi tạo FastAPI app
app = FastAPI(
    title="FastAPI Backend",
    description="Backend API cho ứng dụng web",
    version="1.0.0",
    lifespan=lifespan
)

# Cấu hình CORS để cho phép React frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logger.warning(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI Backend"}


# Include routers
app.include_router(todo_router)

# Import và include routers (sẽ được thêm sau)
# from app.routers import users, items
# app.include_router(users.router)
# app.include_router(items.router) 