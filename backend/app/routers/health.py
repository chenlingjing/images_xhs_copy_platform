from sqlalchemy import text

from fastapi import APIRouter

from ..core.database import engine
from ..core.redis import redis_client
from ..schemas.common import ApiResponse

router = APIRouter(prefix="/health", tags=["健康检查"])


@router.get("", response_model=ApiResponse, response_model_by_alias=True)
async def health_check() -> ApiResponse:
    result = {
        "status": "ok",
        "services": {},
    }

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        result["services"]["mysql"] = "ok"
    except Exception as e:
        result["services"]["mysql"] = f"error: {str(e)}"
        result["status"] = "degraded"

    try:
        await redis_client.ping()
        result["services"]["redis"] = "ok"
    except Exception as e:
        result["services"]["redis"] = f"error: {str(e)}"
        result["status"] = "degraded"

    return ApiResponse(data=result)
