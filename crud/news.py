from fastapi.params import Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from models.news import Category, News


async def get_categories_data(db: AsyncSession, skip: int = 0, limit: int = 10):
    res_sql = select(Category).offset(skip).limit(limit)
    data = await db.execute(res_sql)
    return data.scalars().all()


async def get_news_list_data(db: AsyncSession, category_id: int, page: int = 1, page_size: int = 10):
    res_sql = select(News).where(News.category_id == category_id).offset(page_size * (page - 1)).limit(page_size)
    data = await db.execute(res_sql)
    return data.scalars().all()


async def get_news_list_count(db: AsyncSession, category_id: int):
    res_sql = select(News).where(News.category_id == category_id)
    data = await db.execute(res_sql)
    return len(data.scalars().all())


async def get_news_detail_data(db: AsyncSession, news_id: int):
    res_sql = select(News).where(News.id == news_id)
    data = await db.execute(res_sql)
    if data:
        update_sql = update(News).where(News.id == news_id).values(views=News.views + 1)
        await db.execute(update_sql)
        return data.scalars().first()
    else:
        return ''


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    res_sql = select(News).where(News.category_id == category_id).where(News.id != news_id).limit(limit).order_by(
        News.publish_time.desc())
    data = await db.execute(res_sql)
    return data.scalars().all()
