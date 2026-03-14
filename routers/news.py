from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_categories_data, get_news_list_data, get_news_list_count, get_news_detail_data, \
    get_related_news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    data = await get_categories_data(db, skip, limit)
    return {
        'code': 200,
        'data': data,
        'message': '获取新闻分类成功'
    }


@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db),
        category_id: int = Query(alias='categoryId'),
        page: int = 1,
        page_size: int = Query(le=100, alias='pageSize', default=10)):
    data = await get_news_list_data(db, category_id, page, page_size)
    total = await get_news_list_count(db, category_id)
    has_more = True if total > page_size * page + len(data) else False
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": data,
            "total": total,
            "hasMore": has_more
        }
    }


@router.get("/detail")
async def get_news_detail(db: AsyncSession = Depends(get_db), news_id: int = Query(alias='id')):
    data = await get_news_detail_data(db, news_id)
    if not data:
        raise HTTPException(status_code=404, detail="新闻不存在")
    related_news = await get_related_news(db, data.id, data.category_id, 5)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": data.id,
            "title": data.title,
            "content": data.content,
            "image": data.image,
            "author": data.author,
            "publishTime": data.publish_time,
            "categoryId": data.category_id,
            "views": data.views,
            "relatedNews": related_news
        }
    }
