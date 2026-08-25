from datetime import datetime, timedelta
from urllib.parse import urlparse

from fastapi import APIRouter, Depends
from sqlalchemy import delete, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..core.database import get_db
from ..dependencies.auth import AuthContext, get_current_auth, get_current_user
from ..models.auth_session import AuthSession
from ..models.user import User
from ..schemas.auth import (
    AuthResult,
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    UpdateAvatarRequest,
    UserResponse,
)
from ..schemas.common import ApiResponse
from ..utils.exceptions import AppException, AuthenticationException
from ..utils.security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)


router = APIRouter(prefix="/api/auth", tags=["用户认证"])


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        avatar=user.avatar,
        created_at=user.created_at,
        last_active_at=user.last_active_at,
    )


async def create_login_session(db: AsyncSession, user: User) -> AuthResult:
    token = create_session_token()
    db.add(
        AuthSession(
            token_hash=hash_session_token(token),
            user_id=user.id,
            expires_at=datetime.now() + timedelta(days=settings.SESSION_EXPIRE_DAYS),
        )
    )
    user.last_active_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    return AuthResult(token=token, user=to_user_response(user))


@router.post(
    "/register",
    response_model=ApiResponse[AuthResult],
    response_model_by_alias=True,
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[AuthResult]:
    username = request.username.strip()
    email = request.email.strip().lower()
    existing_result = await db.execute(
        select(User).where(or_(User.username == username, User.email == email))
    )
    existing = existing_result.scalar_one_or_none()
    if existing:
        message = "用户名已被注册" if existing.username == username else "邮箱已被注册"
        raise AppException(code=409, message=message)

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(request.password),
        role="user",
    )
    db.add(user)
    try:
        await db.flush()
        result = await create_login_session(db, user)
    except IntegrityError:
        await db.rollback()
        raise AppException(code=409, message="用户名或邮箱已被注册")
    return ApiResponse(data=result)


@router.post(
    "/login",
    response_model=ApiResponse[AuthResult],
    response_model_by_alias=True,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[AuthResult]:
    account = request.account.strip()
    result = await db.execute(
        select(User).where(
            or_(User.username == account, User.email == account.lower())
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(request.password, user.password_hash):
        raise AuthenticationException("用户名、邮箱或密码错误")

    await db.execute(
        delete(AuthSession).where(AuthSession.expires_at <= datetime.now())
    )
    auth_result = await create_login_session(db, user)
    return ApiResponse(data=auth_result)


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
    response_model_by_alias=True,
)
async def get_me(
    user: User = Depends(get_current_user),
) -> ApiResponse[UserResponse]:
    return ApiResponse(data=to_user_response(user))


@router.post("/logout", response_model=ApiResponse, response_model_by_alias=True)
async def logout(
    auth: AuthContext = Depends(get_current_auth),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    await db.delete(auth.session)
    await db.commit()
    return ApiResponse(message="退出成功")


@router.patch(
    "/avatar",
    response_model=ApiResponse[UserResponse],
    response_model_by_alias=True,
)
async def update_avatar(
    request: UpdateAvatarRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserResponse]:
    avatar = request.avatar.strip()
    if avatar:
        parsed = urlparse(avatar)
        if not avatar.startswith("/uploads/") and parsed.scheme not in {"http", "https"}:
            raise AppException(code=400, message="头像地址无效")
    user.avatar = avatar
    await db.commit()
    await db.refresh(user)
    return ApiResponse(data=to_user_response(user))


@router.post(
    "/change-password",
    response_model=ApiResponse,
    response_model_by_alias=True,
)
async def change_password(
    request: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    if not verify_password(request.old_password, user.password_hash):
        raise AppException(code=400, message="当前密码错误")
    if request.old_password == request.new_password:
        raise AppException(code=400, message="新密码不能与当前密码相同")

    user.password_hash = hash_password(request.new_password)
    await db.commit()
    return ApiResponse(message="密码修改成功")
