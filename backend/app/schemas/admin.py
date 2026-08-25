from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .generate import GenerateResult


class AdminSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DailyStatsResponse(AdminSchema):
    date: str
    total_generations: int
    success_count: int
    failed_count: int
    unique_users: int


class AdminOverviewResponse(AdminSchema):
    total_users: int
    total_generations: int
    today_generations: int
    success_rate: int
    avg_generation_time_ms: int
    daily_stats: list[DailyStatsResponse] = Field(default_factory=list)


class AdminGenerationParams(AdminSchema):
    image_url: str
    product_name: str = ""
    target_audience: str = ""
    tone_style: str = ""


class AdminGenerationUser(AdminSchema):
    id: int
    username: str
    avatar: str = ""


class AdminGenerationResponse(AdminSchema):
    id: int
    image_url: str
    params: AdminGenerationParams
    result: GenerateResult | None = None
    status: Literal["success", "failed"]
    error_message: str = ""
    duration_ms: int = 0
    created_at: datetime
    user: AdminGenerationUser
