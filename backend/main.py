"""
Suraksha — Regulatory Compliance Automation Platform
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from routers import upload, extraction, tasks, verification

# Initialize FastAPI app
app = FastAPI(
    title="Suraksha",
    description="AI-powered regulatory compliance automation for Indian banking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(upload.router)
app.include_router(extraction.router)
app.include_router(tasks.router)
app.include_router(verification.router)


@app.on_event("startup")
async def startup():
    """Initialize database and create upload directory on startup."""
    settings.init()
    init_db()
    print("[Suraksha] API started successfully")
    print(f"[Suraksha] LLM Mode: {settings.LLM_MODE}")
    print(f"[Suraksha] Database: {settings.DATABASE_URL}")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "Suraksha",
        "version": "1.0.0",
        "status": "running",
        "description": "Regulatory Compliance Automation Platform",
        "llm_mode": settings.LLM_MODE
    }


@app.get("/api/health")
async def health():
    """Health check for monitoring."""
    return {"status": "healthy", "llm_mode": settings.LLM_MODE}
