from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..models.generate_record import GenerateRecord
from ..schemas.common import ApiResponse, PageResponse
from ..schemas.generate import (
    GenerateRecordListQuery,
    GenerateRecordResponse,
    GenerateRequest,
    GenerateResult,
)
from ..services.image_service import image_to_base64
from ..services.llm_service import llm_service

router = APIRouter(prefix="/api/generate", tags=["文案生成"])


@router.post("", response_model=ApiResponse, response_model_by_alias=True)
async def generate_copy(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    if request.image_type == 2 and not request.image_url:
        return ApiResponse(code=400, message="URL类型图片必须提供 image_url")

    image_base64 = await image_to_base64(request.image_url, request.image_type)

    llm_result = await llm_service.call_vision(
        image_base64=image_base64,
        product_name=request.product_name,
        target_audience=request.target_audience,
        tone_style=request.tone_style,
    )

    tags = [t.strip() for t in llm_result.get("tags", []) if t]

    record = GenerateRecord(
        image_type=request.image_type,
        image_url=request.image_url,
        product_name=request.product_name,
        target_audience=request.target_audience,
        tone_style=request.tone_style,
        title=llm_result.get("title", ""),
        content=llm_result.get("content", ""),
        tags=",".join(tags),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

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
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    offset = (query.page - 1) * query.page_size

    count_result = await db.execute(select(func.count()).select_from(GenerateRecord))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(GenerateRecord)
        .order_by(GenerateRecord.create_time.desc())
        .offset(offset)
        .limit(query.page_size)
    )
    records = result.scalars().all()

    items = [
        GenerateRecordResponse(
            id=r.id,
            image_type=r.image_type,
            image_url=r.image_url,
            product_name=r.product_name,
            target_audience=r.target_audience,
            tone_style=r.tone_style,
            title=r.title,
            content=r.content,
            tags=r.tags.split(",") if r.tags else [],
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
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    result = await db.execute(
        select(GenerateRecord).where(GenerateRecord.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return ApiResponse(code=404, message="记录不存在")

    data = GenerateRecordResponse(
        id=record.id,
        image_type=record.image_type,
        image_url=record.image_url,
        product_name=record.product_name,
        target_audience=record.target_audience,
        tone_style=record.tone_style,
        title=record.title,
        content=record.content,
        tags=record.tags.split(",") if record.tags else [],
        create_time=record.create_time,
        update_time=record.update_time,
    )
    return ApiResponse(data=data)


@router.delete("/records/{record_id}", response_model=ApiResponse, response_model_by_alias=True)
async def delete_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    result = await db.execute(
        select(GenerateRecord).where(GenerateRecord.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return ApiResponse(code=404, message="记录不存在")

    await db.delete(record)
    await db.commit()
    return ApiResponse(message="删除成功")
