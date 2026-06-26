from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from routers import upload, extraction, tasks, verification

app = FastAPI(
    title="Suraksha",
    description="AI-powered regulatory compliance automation for Indian banking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(extraction.router)
app.include_router(tasks.router)
app.include_router(verification.router)


@app.on_event("startup")
async def startup():
    settings.init()
    init_db()
    print("[Suraksha] API started successfully")
    print(f"[Suraksha] LLM Mode: {settings.LLM_MODE}")
    print(f"[Suraksha] Database: {settings.DATABASE_URL}")


@app.get("/")
async def root():
    return {
        "name": "Suraksha",
        "version": "1.0.0",
        "status": "running",
        "description": "Regulatory Compliance Automation Platform",
        "llm_mode": settings.LLM_MODE
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "llm_mode": settings.LLM_MODE}
