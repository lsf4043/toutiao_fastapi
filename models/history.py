"""
浏览历史模型
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from models.news import Base
# 导入User模型以确保外键可以解析
from models.user import User  # noqa: F401


class History(Base):
    """浏览历史表"""
    __tablename__ = "history"

    # 重写以排除updated_at字段
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="历史记录ID"
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", name="fk_history_user"),
        nullable=False,
        comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("news.id", name="fk_history_news"),
        nullable=False,
        comment="新闻ID"
    )
    view_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="浏览时间"
    )

    # 明确声明不包含updated_at和created_at
    updated_at = None
    created_at = None

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "newsId": self.news_id,
            "viewTime": self.view_time.strftime("%Y-%m-%dT%H:%M:%S") if self.view_time else None
        }
