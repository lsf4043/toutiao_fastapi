from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, Enum
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from models.news import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="用户ID"
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名"
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码（加密存储）"
    )
    nickname: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        default=None,
        comment="昵称"
    )
    avatar: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        comment="头像URL"
    )
    gender: Mapped[str] = mapped_column(
        Enum('male', 'female', 'unknown'),
        nullable=True,
        default='unknown',
        comment="性别"
    )
    bio: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        default=None,
        comment="个人简介"
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        default=None,
        comment="手机号"
    )


class UserToken(Base):
    __tablename__ = "user_token"
    
    # 重写以排除updated_at字段
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="令牌ID"
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        comment="用户ID"
    )
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="令牌值"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="过期时间"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="创建时间"
    )
    
    # 明确声明不包含updated_at
    updated_at = None
