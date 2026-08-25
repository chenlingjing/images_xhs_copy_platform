from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..models.auth_session import AuthSession
from ..models.user import User
from ..utils.exceptions import AuthenticationException, PermissionDeniedException
from ..utils.security import hash_session_token


bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthContext:
    user: User
    session: AuthSession


async def get_current_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> AuthContext:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise AuthenticationException()

    result = await db.execute(
        select(User, AuthSession)
        .join(AuthSession, AuthSession.user_id == User.id)
        .where(AuthSession.token_hash == hash_session_token(credentials.credentials))
    )
    row = result.one_or_none()
    if not row:
        raise AuthenticationException("登录状态已失效，请重新登录")

    user, auth_session = row
    now = datetime.now()
    if auth_session.expires_at <= now:
        await db.delete(auth_session)
        await db.commit()
        raise AuthenticationException("登录状态已过期，请重新登录")

    if user.last_active_at < now - timedelta(minutes=5):
        user.last_active_at = now
        await db.commit()

    return AuthContext(user=user, session=auth_session)


async def get_current_user(
    auth: AuthContext = Depends(get_current_auth),
) -> User:
    return auth.user


async def get_current_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.role != "admin":
        raise PermissionDeniedException("仅管理员可访问")
    return user
