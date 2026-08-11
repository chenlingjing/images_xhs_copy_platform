from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应结构，字段使用 camelCase 序列化"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    code: int = 200
    message: str = "success"
    data: T | None = None


class PageResponse(BaseModel, Generic[T]):
    """分页响应结构，字段使用 camelCase 序列化"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    total: int = 0
    page: int = 1
    page_size: int = 20
    items: list[T] = []
