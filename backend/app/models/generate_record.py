from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class GenerateRecord(Base):
    __tablename__ = "generate_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    image_type: Mapped[int] = mapped_column(Integer, default=1, comment="图片类型：1-本地上传 2-URL链接")
    image_url: Mapped[str] = mapped_column(String(500), default="", comment="图片存储路径/在线URL")
    product_name: Mapped[str] = mapped_column(String(100), default="", comment="产品名称")
    target_audience: Mapped[str] = mapped_column(String(100), default="", comment="目标人群")
    tone_style: Mapped[str] = mapped_column(String(50), default="", comment="语气风格")
    title: Mapped[str] = mapped_column(String(50), default="", comment="生成的小红书标题")
    content: Mapped[str] = mapped_column(Text, default="", comment="生成的小红书正文")
    tags: Mapped[str] = mapped_column(String(200), default="", comment="话题标签，英文逗号分隔")
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    error_message: Mapped[str] = mapped_column(String(500), default="")
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )
