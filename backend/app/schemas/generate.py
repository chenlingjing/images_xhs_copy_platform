from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


ImageType = Literal[1, 2]


class GenerateRequest(BaseModel):
    """文案生成请求，同时兼容 snake_case 和 camelCase"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    image_type: ImageType = Field(default=1, description="图片类型：1-本地上传 2-URL链接")
    image_url: str = Field(default="", max_length=500, description="图片URL（image_type=2时必填）")
    product_name: str = Field(default="", max_length=100, description="产品名称（可选）")
    target_audience: str = Field(default="", max_length=100, description="目标人群（可选）")
    tone_style: str = Field(default="", max_length=50, description="语气风格（可选）")


class GenerateResult(BaseModel):
    """文案生成结果"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: int = Field(default=0, description="生成记录ID")
    title: str = Field(default="", max_length=50, description="小红书标题")
    content: str = Field(default="", description="小红书正文")
    tags: list[str] = Field(default_factory=list, description="话题标签列表")


class GenerateRecordResponse(BaseModel):
    """生成记录响应"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: int
    user_id: int | None = None
    image_type: int
    image_url: str
    product_name: str
    target_audience: str
    tone_style: str
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    status: Literal["pending", "success", "failed"]
    error_message: str = ""
    duration_ms: int = 0
    create_time: datetime
    update_time: datetime


class GenerateRecordListQuery(BaseModel):
    """生成记录列表查询参数"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
