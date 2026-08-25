from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from . import models  # noqa: F401
from .core.config import UPLOAD_DIR, settings
from .core.database import Base, engine
from .core.redis import redis_client
from .core.schema import seed_initial_admin, upgrade_schema
from .routers.admin import router as admin_router
from .routers.auth import router as auth_router
from .routers.generate import router as generate_router
from .routers.health import router as health_router
from .routers.images import router as images_router
from .utils.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await upgrade_schema()
    await seed_initial_admin()
    try:
        await redis_client.ping()
    except Exception:
        pass
    yield
    await engine.dispose()
    try:
        await redis_client.close()
    except Exception:
        pass


app = FastAPI(
    title="小红书文案生成平台 - 后端 API",
    description="基于多模态大模型的小红书文案生成平台后端服务",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误，请稍后重试", "data": None},
    )


app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(images_router)
app.include_router(generate_router)
app.include_router(admin_router)


@app.get("/", tags=["根路径"])
async def root() -> dict:
    return {
        "name": "小红书文案生成平台 API",
        "version": "1.0.0",
        "docs": "/docs",
    }
