from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from models.news import Base


class Favorite(Base):
    __tablename__ = "favorite"
    
    # 重写以排除updated_at字段
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="收藏ID"
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("user.id"),
        nullable=False,
        comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("news.id"),
        nullable=False,
        comment="新闻ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="收藏时间"
    )
    
    # 明确声明不包含updated_at
    updated_at = None
