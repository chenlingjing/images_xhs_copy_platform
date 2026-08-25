import logging

from sqlalchemy import select, text

from ..models.user import User
from ..utils.security import hash_password
from .config import settings
from .database import AsyncSessionLocal, engine


logger = logging.getLogger(__name__)

GENERATE_RECORD_COLUMNS = {
    "user_id": "BIGINT NULL AFTER id",
    "status": "VARCHAR(20) NOT NULL DEFAULT 'success' AFTER tags",
    "error_message": "VARCHAR(500) NOT NULL DEFAULT '' AFTER status",
    "duration_ms": "INT NOT NULL DEFAULT 0 AFTER error_message",
}


async def upgrade_schema() -> None:
    """Apply the small, idempotent upgrade needed by pre-migration databases."""
    async with engine.begin() as connection:
        result = await connection.execute(
            text(
                """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :database_name
                  AND TABLE_NAME = 'generate_record'
                """
            ),
            {"database_name": settings.MYSQL_DATABASE},
        )
        existing_columns = {row[0] for row in result}

        for column_name, definition in GENERATE_RECORD_COLUMNS.items():
            if column_name not in existing_columns:
                await connection.execute(
                    text(
                        f"ALTER TABLE generate_record "
                        f"ADD COLUMN {column_name} {definition}"
                    )
                )

        index_result = await connection.execute(
            text(
                """
                SELECT INDEX_NAME
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = :database_name
                  AND TABLE_NAME = 'generate_record'
                """
            ),
            {"database_name": settings.MYSQL_DATABASE},
        )
        existing_indexes = {row[0] for row in index_result}
        if not {"ix_generate_record_user_id", "idx_generate_user_id"} & existing_indexes:
            await connection.execute(
                text(
                    "CREATE INDEX ix_generate_record_user_id "
                    "ON generate_record (user_id)"
                )
            )
        if not {"ix_generate_record_status", "idx_generate_status"} & existing_indexes:
            await connection.execute(
                text(
                    "CREATE INDEX ix_generate_record_status "
                    "ON generate_record (status)"
                )
            )

        foreign_key_count = await connection.scalar(
            text(
                """
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = :database_name
                  AND TABLE_NAME = 'generate_record'
                  AND COLUMN_NAME = 'user_id'
                  AND REFERENCED_TABLE_NAME = 'users'
                """
            ),
            {"database_name": settings.MYSQL_DATABASE},
        )
        if not foreign_key_count:
            await connection.execute(
                text(
                    "ALTER TABLE generate_record "
                    "ADD CONSTRAINT fk_generate_record_user "
                    "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL"
                )
            )

        await connection.execute(
            text(
                """
                UPDATE generate_record
                SET status = 'failed',
                    error_message = '生成任务意外中断'
                WHERE status = 'pending'
                """
            )
        )


async def seed_initial_admin() -> None:
    username = settings.INITIAL_ADMIN_USERNAME.strip()
    email = settings.INITIAL_ADMIN_EMAIL.strip().lower()
    password = settings.INITIAL_ADMIN_PASSWORD
    if not username or not email or not password:
        return
    if len(password) < 8:
        logger.warning("INITIAL_ADMIN_PASSWORD must contain at least 8 characters")
        return

    async with AsyncSessionLocal() as session:
        username_user = (
            await session.execute(select(User).where(User.username == username))
        ).scalar_one_or_none()
        email_user = (
            await session.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()

        if username_user and email_user and username_user.id != email_user.id:
            logger.warning(
                "Initial administrator username and email belong to different users"
            )
            return

        existing_user = username_user or email_user
        if existing_user:
            if existing_user.role == "admin":
                return
            existing_user.username = username
            existing_user.email = email
            existing_user.password_hash = hash_password(password)
            existing_user.role = "admin"
            await session.commit()
            logger.info("Existing user promoted to initial administrator")
            return

        session.add(
            User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role="admin",
            )
        )
        await session.commit()
        logger.info("Initial administrator account created")
