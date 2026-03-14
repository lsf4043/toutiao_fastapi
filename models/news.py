from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, Index, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="更新时间"
    )


class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="分类id"
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="分类名称"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="排序"
    )

class News(Base):
    __tablename__ = "news"

    __table_args__ = (
        Index('news_category_id', 'category_id'),
        Index('news_publish_time', 'publish_time'),
    )

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="新闻id"
    )
    title: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="新闻标题"
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="新闻描述"
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="新闻内容"
    )
    image: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="新闻图片"
    )
    author: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="新闻作者"
    )
    category_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("news_category.id"),
        nullable=False,
        comment="新闻分类id"
    )
    views: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        default=0,
        nullable=False,
        comment="新闻浏览量"
    )
    publish_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="新闻发布时间"
    )
