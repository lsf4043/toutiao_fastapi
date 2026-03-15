from datetime import datetime
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from models.favorite import Favorite
from models.news import News


async def check_favorite(db: AsyncSession, user_id: int, news_id: int):
    """检查是否已收藏"""
    result = await db.execute(
        select(Favorite).where(
            and_(Favorite.user_id == user_id, Favorite.news_id == news_id)
        )
    )
    return result.scalars().first() is not None


async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    """添加收藏"""
    favorite = Favorite(
        user_id=user_id,
        news_id=news_id,
        created_at=datetime.now()
    )
    db.add(favorite)
    await db.flush()
    return favorite


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    """取消收藏"""
    result = await db.execute(
        delete(Favorite).where(
            and_(Favorite.user_id == user_id, Favorite.news_id == news_id)
        )
    )
    return result.rowcount > 0


async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """获取收藏列表"""
    # 查询收藏的新闻
    offset = (page - 1) * page_size
    
    # 联表查询收藏和新闻信息
    query = (
        select(Favorite, News)
        .join(News, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    # 格式化返回数据
    favorites = []
    for favorite, news in rows:
        favorites.append({
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "publishTime": news.publish_time,
            "categoryId": news.category_id,
            "views": news.views,
            "favoriteTime": favorite.created_at
        })
    
    return favorites


async def get_favorite_count(db: AsyncSession, user_id: int):
    """获取收藏总数"""
    result = await db.execute(
        select(count(Favorite.id)).where(Favorite.user_id == user_id)
    )
    return result.scalar()


async def clear_favorites(db: AsyncSession, user_id: int):
    """清空所有收藏"""
    result = await db.execute(
        delete(Favorite).where(Favorite.user_id == user_id)
    )
    return result.rowcount
