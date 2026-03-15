from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from config.db_conf import get_db
from crud import favorite as favorite_crud
from routers.user import get_current_user

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 请求模型
class FavoriteAddRequest(BaseModel):
    newsId: int


@router.get("/check")
async def check_favorite(
    newsId: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """检查新闻收藏状态"""
    is_favorite = await favorite_crud.check_favorite(db, current_user.id, newsId)
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "isFavorite": is_favorite
        }
    }


@router.post("/add")
async def add_favorite(
    request: FavoriteAddRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加收藏"""
    # 检查是否已收藏
    is_exists = await favorite_crud.check_favorite(db, current_user.id, request.newsId)
    if is_exists:
        return {
            "code": 400,
            "message": "已收藏该新闻",
            "data": None
        }
    
    # 添加收藏
    favorite = await favorite_crud.add_favorite(db, current_user.id, request.newsId)
    
    return {
        "code": 200,
        "message": "收藏成功",
        "data": {
            "id": favorite.id,
            "userId": favorite.user_id,
            "newsId": favorite.news_id,
            "createTime": favorite.created_at
        }
    }


@router.delete("/remove")
async def remove_favorite(
    newsId: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏"""
    success = await favorite_crud.remove_favorite(db, current_user.id, newsId)
    
    if not success:
        return {
            "code": 400,
            "message": "未收藏该新闻",
            "data": None
        }
    
    return {
        "code": 200,
        "message": "取消收藏成功",
        "data": None
    }


@router.get("/list")
async def get_favorite_list(
    page: int = 1,
    pageSize: int = 10,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取收藏列表"""
    # 限制pageSize最大值
    if pageSize > 100:
        pageSize = 100
    
    # 获取收藏列表
    favorites = await favorite_crud.get_favorite_list(db, current_user.id, page, pageSize)
    
    # 获取总数
    total = await favorite_crud.get_favorite_count(db, current_user.id)
    
    # 计算是否有更多
    has_more = total > page * pageSize
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": favorites,
            "total": total,
            "hasMore": has_more
        }
    }


@router.delete("/clear")
async def clear_favorites(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空所有收藏"""
    count = await favorite_crud.clear_favorites(db, current_user.id)
    
    return {
        "code": 200,
        "message": f"成功删除{count}条收藏记录",
        "data": None
    }
