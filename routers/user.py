from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from config.db_conf import get_db
from crud import user as user_crud

router = APIRouter(prefix="/api/user", tags=["user"])


# 请求模型
class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


class PasswordUpdateRequest(BaseModel):
    oldPassword: str
    newPassword: str


# 依赖项：获取当前用户
async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    user = await user_crud.get_user_by_token(db, authorization)
    if not user:
        raise HTTPException(status_code=401, detail="无效的认证令牌或令牌已过期")
    
    return user


@router.post("/register")
async def register(request: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = await user_crud.get_user_by_username(db, request.username)
    if existing_user:
        return {
            "code": 400,
            "message": "用户名已存在",
            "data": None
        }
    
    # 创建用户
    user = await user_crud.create_user(db, request.username, request.password)
    
    # 创建token
    token = await user_crud.create_token(db, user.id)
    
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }


@router.post("/login")
async def login(request: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    # 查询用户
    user = await user_crud.get_user_by_username(db, request.username)
    if not user:
        return {
            "code": 400,
            "message": "用户名或密码错误",
            "data": None
        }
    
    # 验证密码
    if not await user_crud.verify_password(request.password, user.password):
        return {
            "code": 400,
            "message": "用户名或密码错误",
            "data": None
        }
    
    # 创建token
    token = await user_crud.create_token(db, user.id)
    
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "bio": user.bio
            }
        }
    }


@router.get("/info")
async def get_user_info(
    current_user = Depends(get_current_user)
):
    """获取用户信息"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "gender": current_user.gender,
            "bio": current_user.bio
        }
    }


@router.put("/update")
async def update_user(
    request: UserUpdateRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    # 更新用户信息
    updated_user = await user_crud.update_user_info(
        db,
        current_user.id,
        nickname=request.nickname,
        avatar=request.avatar,
        gender=request.gender,
        bio=request.bio,
        phone=request.phone
    )
    
    if not updated_user:
        return {
            "code": 400,
            "message": "更新失败",
            "data": None
        }
    
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "id": updated_user.id,
            "username": updated_user.username,
            "nickname": updated_user.nickname,
            "avatar": updated_user.avatar,
            "gender": updated_user.gender,
            "bio": updated_user.bio
        }
    }


@router.put("/password")
async def update_password(
    request: PasswordUpdateRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改用户密码"""
    # 验证旧密码
    if not await user_crud.verify_password(request.oldPassword, current_user.password):
        return {
            "code": 400,
            "message": "原密码错误",
            "data": None
        }
    
    # 更新密码
    await user_crud.update_user_password(db, current_user.id, request.newPassword)
    
    return {
        "code": 200,
        "message": "密码修改成功",
        "data": None
    }
