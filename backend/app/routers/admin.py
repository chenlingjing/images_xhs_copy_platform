from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..dependencies.auth import get_current_admin
from ..models.generate_record import GenerateRecord
from ..models.user import User
from ..schemas.admin import (
    AdminGenerationParams,
    AdminGenerationResponse,
    AdminGenerationUser,
    AdminOverviewResponse,
    DailyStatsResponse,
)
from ..schemas.auth import UserResponse
from ..schemas.common import ApiResponse
from ..schemas.generate import GenerateResult


router = APIRouter(
    prefix="/api/admin",
    tags=["后台管理"],
    dependencies=[Depends(get_current_admin)],
)


@router.get(
    "/overview",
    response_model=ApiResponse[AdminOverviewResponse],
    response_model_by_alias=True,
)
async def get_overview(
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[AdminOverviewResponse]:
    today = date.today()
    start_date = today - timedelta(days=13)
    start_datetime = datetime.combine(start_date, time.min)
    today_start = datetime.combine(today, time.min)
    tomorrow_start = today_start + timedelta(days=1)

    total_users = (
        await db.execute(select(func.count()).select_from(User))
    ).scalar_one()
    total_generations = (
        await db.execute(select(func.count()).select_from(GenerateRecord))
    ).scalar_one()
    today_generations = (
        await db.execute(
            select(func.count())
            .select_from(GenerateRecord)
            .where(
                GenerateRecord.create_time >= today_start,
                GenerateRecord.create_time < tomorrow_start,
            )
        )
    ).scalar_one()
    success_count = (
        await db.execute(
            select(func.count())
            .select_from(GenerateRecord)
            .where(GenerateRecord.status == "success")
        )
    ).scalar_one()
    avg_duration = (
        await db.execute(
            select(func.avg(GenerateRecord.duration_ms)).where(
                GenerateRecord.status == "success"
            )
        )
    ).scalar_one()

    daily_result = await db.execute(
        select(
            func.date(GenerateRecord.create_time).label("day"),
            func.count(GenerateRecord.id).label("total"),
            func.sum(
                case((GenerateRecord.status == "success", 1), else_=0)
            ).label("successful"),
            func.sum(
                case((GenerateRecord.status == "failed", 1), else_=0)
            ).label("failed"),
            func.count(func.distinct(GenerateRecord.user_id)).label("users"),
        )
        .where(GenerateRecord.create_time >= start_datetime)
        .group_by(func.date(GenerateRecord.create_time))
        .order_by(func.date(GenerateRecord.create_time))
    )
    rows_by_date = {str(row.day): row for row in daily_result}

    daily_stats = []
    for offset in range(14):
        current_date = start_date + timedelta(days=offset)
        row = rows_by_date.get(current_date.isoformat())
        daily_stats.append(
            DailyStatsResponse(
                date=current_date.isoformat(),
                total_generations=int(row.total or 0) if row else 0,
                success_count=int(row.successful or 0) if row else 0,
                failed_count=int(row.failed or 0) if row else 0,
                unique_users=int(row.users or 0) if row else 0,
            )
        )

    success_rate = (
        round((success_count / total_generations) * 100)
        if total_generations
        else 0
    )
    overview = AdminOverviewResponse(
        total_users=total_users,
        total_generations=total_generations,
        today_generations=today_generations,
        success_rate=success_rate,
        avg_generation_time_ms=round(float(avg_duration or 0)),
        daily_stats=daily_stats,
    )
    return ApiResponse(data=overview)


@router.get(
    "/users",
    response_model=ApiResponse[list[UserResponse]],
    response_model_by_alias=True,
)
async def list_users(
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[list[UserResponse]]:
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return ApiResponse(
        data=[
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                avatar=user.avatar,
                created_at=user.created_at,
                last_active_at=user.last_active_at,
            )
            for user in users
        ]
    )


@router.get(
    "/generations",
    response_model=ApiResponse[list[AdminGenerationResponse]],
    response_model_by_alias=True,
)
async def list_generations(
    page_size: int = Query(default=100, ge=1, le=500, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[list[AdminGenerationResponse]]:
    result = await db.execute(
        select(GenerateRecord, User)
        .outerjoin(User, User.id == GenerateRecord.user_id)
        .order_by(GenerateRecord.create_time.desc())
        .limit(page_size)
    )

    items = []
    for record, user in result.all():
        status = "success" if record.status == "success" else "failed"
        generation_result = None
        if status == "success":
            generation_result = GenerateResult(
                id=record.id,
                title=record.title,
                content=record.content,
                tags=record.tags.split(",") if record.tags else [],
            )
        items.append(
            AdminGenerationResponse(
                id=record.id,
                image_url=record.image_url,
                params=AdminGenerationParams(
                    image_url=record.image_url,
                    product_name=record.product_name,
                    target_audience=record.target_audience,
                    tone_style=record.tone_style,
                ),
                result=generation_result,
                status=status,
                error_message=record.error_message,
                duration_ms=record.duration_ms,
                created_at=record.create_time,
                user=AdminGenerationUser(
                    id=user.id if user else 0,
                    username=user.username if user else "历史记录",
                    avatar=user.avatar if user else "",
                ),
            )
        )
    return ApiResponse(data=items)


@router.delete(
    "/generations/{record_id}",
    response_model=ApiResponse,
    response_model_by_alias=True,
)
async def delete_generation(
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
