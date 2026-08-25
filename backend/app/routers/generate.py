from time import perf_counter

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..dependencies.auth import get_current_user
from ..models.generate_record import GenerateRecord
from ..models.user import User
from ..schemas.common import ApiResponse, PageResponse
from ..schemas.generate import (
    GenerateRecordListQuery,
    GenerateRecordResponse,
    GenerateRequest,
    GenerateResult,
)
from ..services.image_service import image_to_base64
from ..services.llm_service import llm_service
from ..utils.exceptions import AppException

router = APIRouter(prefix="/api/generate", tags=["文案生成"])


@router.post("", response_model=ApiResponse, response_model_by_alias=True)
async def generate_copy(
    request: GenerateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    started_at = perf_counter()
    record = GenerateRecord(
        user_id=user.id,
        image_type=request.image_type,
        image_url=request.image_url,
        product_name=request.product_name,
        target_audience=request.target_audience,
        tone_style=request.tone_style,
        status="pending",
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    try:
        if request.image_type == 2 and not request.image_url:
            raise AppException(code=400, message="URL类型图片必须提供 image_url")

        image_base64 = await image_to_base64(request.image_url, request.image_type)
        llm_result = await llm_service.call_vision(
            image_base64=image_base64,
            product_name=request.product_name,
            target_audience=request.target_audience,
            tone_style=request.tone_style,
        )

        tags = [t.strip() for t in llm_result.get("tags", []) if t]
        record.title = llm_result.get("title", "")
        record.content = llm_result.get("content", "")
        record.tags = ",".join(tags)
        record.status = "success"
        record.duration_ms = int((perf_counter() - started_at) * 1000)
        await db.commit()
        await db.refresh(record)
    except Exception as exc:
        await db.rollback()
        record.status = "failed"
        record.error_message = (
            exc.message if isinstance(exc, AppException) else "文案生成失败，请稍后重试"
        )
        record.duration_ms = int((perf_counter() - started_at) * 1000)
        await db.commit()
        raise

    result = GenerateResult(
        id=record.id,
        title=record.title,
        content=record.content,
        tags=record.tags.split(",") if record.tags else [],
    )
    return ApiResponse(data=result)


@router.get("/records", response_model=ApiResponse, response_model_by_alias=True)
async def list_records(
    query: GenerateRecordListQuery = Depends(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    offset = (query.page - 1) * query.page_size

    user_filter = GenerateRecord.user_id == user.id
    count_result = await db.execute(
        select(func.count()).select_from(GenerateRecord).where(user_filter)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(GenerateRecord)
        .where(user_filter)
        .order_by(GenerateRecord.create_time.desc())
        .offset(offset)
        .limit(query.page_size)
    )
    records = result.scalars().all()

    items = [
        GenerateRecordResponse(
            id=r.id,
            user_id=r.user_id,
            image_type=r.image_type,
            image_url=r.image_url,
            product_name=r.product_name,
            target_audience=r.target_audience,
            tone_style=r.tone_style,
            title=r.title,
            content=r.content,
            tags=r.tags.split(",") if r.tags else [],
            status=r.status,
            error_message=r.error_message,
            duration_ms=r.duration_ms,
            create_time=r.create_time,
            update_time=r.update_time,
        )
        for r in records
    ]

    page = PageResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=items,
    )
    return ApiResponse(data=page)


@router.get("/records/{record_id}", response_model=ApiResponse, response_model_by_alias=True)
async def get_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    result = await db.execute(
        select(GenerateRecord).where(
            GenerateRecord.id == record_id,
            GenerateRecord.user_id == user.id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        return ApiResponse(code=404, message="记录不存在")

    data = GenerateRecordResponse(
        id=record.id,
        user_id=record.user_id,
        image_type=record.image_type,
        image_url=record.image_url,
        product_name=record.product_name,
        target_audience=record.target_audience,
        tone_style=record.tone_style,
        title=record.title,
        content=record.content,
        tags=record.tags.split(",") if record.tags else [],
        status=record.status,
        error_message=record.error_message,
        duration_ms=record.duration_ms,
        create_time=record.create_time,
        update_time=record.update_time,
    )
    return ApiResponse(data=data)


@router.delete("/records/{record_id}", response_model=ApiResponse, response_model_by_alias=True)
async def delete_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    result = await db.execute(
        select(GenerateRecord).where(
            GenerateRecord.id == record_id,
            GenerateRecord.user_id == user.id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        return ApiResponse(code=404, message="记录不存在")

    await db.delete(record)
    await db.commit()
    return ApiResponse(message="删除成功")
