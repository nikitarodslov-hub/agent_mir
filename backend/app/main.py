"""
FastAPI приложение для платформы "Семейные корни"
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.services.graph_engine import GraphEngine
from app.services.fuzzy_matching import FuzzyMatcher
from app.db.postgres import init_db, get_db_session
from app.routes import auth, genealogy, search, gamification, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация сервисов
graph_engine = None
fuzzy_matcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    global graph_engine, fuzzy_matcher

    # Startup
    try:
        graph_engine = GraphEngine(
            settings.NEO4J_URI,
            settings.NEO4J_USER,
            settings.NEO4J_PASSWORD
        )
        fuzzy_matcher = FuzzyMatcher()
        init_db()
        logger.info("✅ Сервисы инициализированы успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации: {e}")

    yield

    # Shutdown
    if graph_engine:
        graph_engine.close()
    logger.info("🔌 Сервисы остановлены")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Платформа для автоматизации генеалогических исследований",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

app.include_router(
    genealogy.router,
    prefix=f"{settings.API_V1_STR}/genealogy",
    tags=["Genealogy"]
)

app.include_router(
    search.router,
    prefix=f"{settings.API_V1_STR}/search",
    tags=["Search"]
)

app.include_router(
    gamification.router,
    prefix=f"{settings.API_V1_STR}/gamification",
    tags=["Gamification"]
)

app.include_router(
    admin.router,
    prefix=f"{settings.API_V1_STR}/admin",
    tags=["Admin"]
)

@app.get("/")
async def root():
    """Проверка здоровья приложения"""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get(f"{settings.API_V1_STR}/stats")
async def get_platform_stats():
    """Получить статистику платформы"""
    try:
        return {
            "total_users": 1000,
            "total_persons": 1500000,
            "total_relationships": 3000000,
            "active_today": 250,
            "api_status": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
