from datetime import datetime, timedelta
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import bcrypt

from models.user import User, UserToken


async def get_user_by_username(db: AsyncSession, username: str):
    """根据用户名获取用户"""
    res_sql = select(User).where(User.username == username)
    result = await db.execute(res_sql)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    """根据用户ID获取用户"""
    res_sql = select(User).where(User.id == user_id)
    result = await db.execute(res_sql)
    return result.scalars().first()


async def create_user(db: AsyncSession, username: str, password: str):
    """创建用户"""
    # 对密码进行加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 创建用户
    user = User(
        username=username,
        password=hashed_password,
        bio="这个人很懒,什么都没留下",
        avatar="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    )
    db.add(user)
    await db.flush()
    return user


async def verify_password(plain_password: str, hashed_password: str):
    """验证密码"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def create_token(db: AsyncSession, user_id: int):
    """创建用户令牌"""
    # 生成唯一token
    token = str(uuid.uuid4())
    # 设置过期时间为30天后
    expires_at = datetime.now() + timedelta(days=30)
    
    user_token = UserToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(user_token)
    await db.flush()
    return token


async def get_user_by_token(db: AsyncSession, token: str):
    """根据token获取用户"""
    # 查询token记录
    token_sql = select(UserToken).where(UserToken.token == token)
    token_result = await db.execute(token_sql)
    user_token = token_result.scalars().first()
    
    if not user_token:
        return None
    
    # 检查token是否过期
    if user_token.expires_at < datetime.now():
        return None
    
    # 获取用户信息
    user = await get_user_by_id(db, user_token.user_id)
    return user


async def update_user_info(db: AsyncSession, user_id: int, **kwargs):
    """更新用户信息"""
    # 过滤掉None值
    update_data = {k: v for k, v in kwargs.items() if v is not None}
    
    if not update_data:
        return None
    
    # 执行更新
    update_sql = update(User).where(User.id == user_id).values(**update_data)
    await db.execute(update_sql)
    
    # 返回更新后的用户信息
    return await get_user_by_id(db, user_id)


async def update_user_password(db: AsyncSession, user_id: int, new_password: str):
    """更新用户密码"""
    # 对新密码进行加密
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 执行更新
    update_sql = update(User).where(User.id == user_id).values(password=hashed_password)
    await db.execute(update_sql)
    
    return True
