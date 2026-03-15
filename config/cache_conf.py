import json
from typing import Any

import redis.asyncio as redis

redis_client = redis.Redis(host="localhost",
                           port=6379,
                           db=0,
                           decode_responses=True,
                           password="123456")


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
