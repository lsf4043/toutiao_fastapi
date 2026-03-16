import sys

sys.path.insert(0, r'/toutiao')

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.user import User
import bcrypt

ASYNC_DATABASE_URL = "mysql+aiomysql://root:Xiliu4043*.@101.200.137.199:3306/news_app?charset=utf8mb4"


async def test_create_user():
    try:
        # 创建异步引擎
        engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

        # 创建会话
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # 测试查询用户
            print("查询用户test123...")
            result = await session.execute(select(User).where(User.username == "test123"))
            user = result.scalars().first()

            if user:
                print(f"用户已存在: {user.username}")
            else:
                print("用户不存在,创建新用户...")
                # 创建用户
                hashed_password = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = User(
                    username="test123",
                    password=hashed_password,
                    bio="这个人很懒,什么都没留下",
                    avatar="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
                )
                session.add(new_user)
                await session.flush()
                print(f"用户创建成功! ID: {new_user.id}, Username: {new_user.username}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_create_user())
