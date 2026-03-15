import sys
sys.path.insert(0, r'/toutiao')

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from toutiao.config.db_conf import get_db
from toutiao.crud import user as user_crud

async def test_register():
    try:
        # 模拟数据库会话
        async for db in get_db():
            print("测试用户注册...")
            
            # 检查用户是否存在
            existing_user = await user_crud.get_user_by_username(db, "testuser_api")
            print(f"用户是否存在: {existing_user}")
            
            if not existing_user:
                # 创建用户
                user = await user_crud.create_user(db, "testuser_api", "123456")
                print(f"用户创建成功: ID={user.id}, Username={user.username}")
                
                # 创建token
                token = await user_crud.create_token(db, user.id)
                print(f"Token创建成功: {token}")
                
                # 提交事务
                await db.commit()
                print("事务提交成功!")
            else:
                print("用户已存在")
                
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_register())
