import json
import os
from typing import Any

import redis.asyncio as redis

# 从环境变量获取Redis配置,支持Docker部署
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "123456")

redis_client = redis.Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           db=0,
                           decode_responses=True,
                           password=REDIS_PASSWORD)


async def get_value(key: str):
    try:
        value = await redis_client.get(key)
        return value
    except Exception as e:
        print(f'获取redis值失败：{e}')
        return None


async def get_json_value(key: str):
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)
    except Exception as e:
        print(f'获取json格式的redis值失败：{e}')
        return None


async def set_value(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.set(key, value, expire)
        return True
    except Exception as e:
        print(f'设置redis值失败：{e}')
        return False
