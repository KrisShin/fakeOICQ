import json
import random
import string
import time
from datetime import timedelta
from pydantic import BaseModel

from redis import asyncio

from config.create_app import app
from config.settings import CACHE_HEADER, REDIS_URL, TIME_NS
from modules.common.global_variable import redis_client


def generate_random_id(count: int = 32) -> str:
    """generate random string length in count."""
    if count < TIME_NS:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=count))

    return str(time.time_ns())[:TIME_NS] + ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=count - TIME_NS)
    )


async def set_cache(key: str, value, ex: timedelta = None) -> bool:
    if not all((key, value)):
        return False

    params = {'name': CACHE_HEADER + key, 'value': value}
    if ex:
        params['ex'] = ex

    global redis_client
    redis_client = await get_redis()
    if isinstance(value, int | float | str):
        return await redis_client.set(**params)
    else:
        try:
            params['value'] = json.dumps(value)
            return await redis_client.set(**params)
        except json.JSONDecodeError:
            return False


async def get_cache(key: str) -> str:
    global redis_client
    redis_client = await get_redis()
    return await redis_client.get(CACHE_HEADER + key)


async def del_cache(key: str) -> str:
    global redis_client
    redis_client = await get_redis()
    return await redis_client.delete(CACHE_HEADER + key)


async def get_redis():
    global redis_client
    if redis_client:
        pong = await redis_client.ping()
        if pong:
            return redis_client
    redis_client = await asyncio.from_url(
        REDIS_URL, decode_responses=True, encoding="utf8"
    )
    return redis_client


def queryset_to_pydantic_model(queryset, model_class):
    return [model_class.model_validate(item) for item in queryset]
