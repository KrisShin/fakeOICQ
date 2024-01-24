from datetime import timedelta
import json
from redis import asyncio

from config.settings import CACHE_HEADER, REDIS_URL
from modules.common.pydantics import UserOpration


class RedisCache:
    redis_client = None

    def __init__(self):
        self.client = self.get_redis()

    async def get_redis(self):
        if self.client:
            pong = await self.client.ping()
            if pong:
                return self.client
        self.client = await asyncio.from_url(
            REDIS_URL, decode_responses=True, encoding="utf8"
        )
        return self.client

    async def set_cache(self, key: str, value, ex: timedelta = None) -> bool:
        if not all((key, value)):
            return False

        params = {'name': CACHE_HEADER + key, 'value': value}
        if ex:
            params['ex'] = ex

        if isinstance(value, int | float | str):
            return await self.client.set(**params)
        else:
            try:
                params['value'] = json.dumps(value)
                return await self.client.set(**params)
            except json.JSONDecodeError:
                return False

    async def get_cache(self, key: str) -> str:
        return await self.client.get(CACHE_HEADER + key)

    async def del_cache(self, key: str) -> str:
        return await self.client.delete(CACHE_HEADER + key)

    async def incr_cache(self, user_id: str, operation_type: UserOpration) -> str:
        key = self.generate_user_operation_key(user_id, operation_type)
        times = await self.client.incr(CACHE_HEADER + key)
        await self.client.expire(CACHE_HEADER + key, operation_type.value.expire)
        return times

    async def clear_cache(self) -> str:
        return await self.client.flushall()

    def generate_user_operation_key(self, user_id: str, operation_type: UserOpration):
        return f"{user_id}.{operation_type.value.code}"


rcache = RedisCache()
