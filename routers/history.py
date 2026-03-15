"""
浏览历史API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from config.db_conf import get_db
from crud import history as history_crud
from routers.user import get_current_user

router = APIRouter(prefix="/api/history", tags=["浏览历史"])


class AddHistoryRequest(BaseModel):
    """添加浏览记录请求"""
    newsId: int


@router.post("/add")
async def add_history(
    request: AddHistoryRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加浏览记录"""
    # 添加浏览记录
    history = await history_crud.add_history(db, current_user.id, request.newsId)

    return {
        "code": 200,
        "message": "添加成功",
        "data": history.to_dict()
    }


@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页条数"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取浏览历史列表"""
    # 获取浏览历史列表
    result = await history_crud.get_history_list(db, current_user.id, page, pageSize)
    await db.commit()

    return {
        "code": 200,
        "message": "success",
        "data": result
    }


@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除单条浏览记录"""
    # 删除浏览记录
    success = await history_crud.delete_history(db, current_user.id, history_id)
    await db.commit()

    if not success:
        raise HTTPException(status_code=400, detail="浏览记录不存在")

    return {
        "code": 200,
        "message": "删除成功",
        "data": None
    }


@router.delete("/clear")
async def clear_history(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空浏览历史"""
    # 清空浏览历史
    count = await history_crud.clear_history(db, current_user.id)
    await db.commit()

    return {
        "code": 200,
        "message": f"清空成功,共删除{count}条记录",
        "data": None
    }
