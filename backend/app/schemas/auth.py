import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class AuthSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class LoginRequest(AuthSchema):
    account: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(AuthSchema):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[\w\u4e00-\u9fff-]+$")
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("邮箱格式不正确")
        return email


class ChangePasswordRequest(AuthSchema):
    old_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


class UpdateAvatarRequest(AuthSchema):
    avatar: str = Field(default="", max_length=500)


class UserResponse(AuthSchema):
    id: int
    username: str
    email: str
    role: Literal["user", "admin"]
    avatar: str = ""
    created_at: datetime
    last_active_at: datetime


class AuthResult(AuthSchema):
    token: str
    user: UserResponse
