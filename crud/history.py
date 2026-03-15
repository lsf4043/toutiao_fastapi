"""
浏览历史CRUD操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from models.history import History
from models.news import News
from datetime import datetime
from typing import List, Dict, Any, Optional


async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    """添加浏览记录"""
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.flush()
    await db.refresh(history)
    return history


async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """获取浏览历史列表"""
    # 限制page_size最大值
    if page_size > 100:
        page_size = 100

    # 查询总数
    count_query = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # 查询列表(联表查询新闻信息)
    query = (select(History, News)
             .join(News, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset((page - 1) * page_size)
             .limit(page_size))

    result = await db.execute(query)
    rows = result.all()

    # 格式化数据
    history_list = []
    for history, news in rows:
        history_list.append({
            "id": history.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "publishTime": news.publish_time.strftime("%Y-%m-%dT%H:%M:%S") if news.publish_time else None,
            "categoryId": news.category_id,
            "views": news.views,
            "viewTime": history.view_time.strftime("%Y-%m-%dT%H:%M:%S") if history.view_time else None
        })

    # 计算是否有更多数据
    has_more = (page * page_size) < total

    return {
        "list": history_list,
        "total": total,
        "hasMore": has_more
    }


async def delete_history(db: AsyncSession, user_id: int, history_id: int) -> bool:
    """删除单条浏览记录"""
    query = delete(History).where(History.id == history_id, History.user_id == user_id)
    result = await db.execute(query)
    await db.flush()
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int) -> int:
    """清空浏览历史"""
    # 先查询总数
    count_query = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # 删除所有记录
    query = delete(History).where(History.user_id == user_id)
    await db.execute(query)
    await db.flush()

    return total


async def get_history_by_id(db: AsyncSession, history_id: int) -> Optional[History]:
    """根据ID获取浏览记录"""
    query = select(History).where(History.id == history_id)
    result = await db.execute(query)
    return result.scalars().first()
