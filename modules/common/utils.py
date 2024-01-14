import json
import random
import string
import time
from datetime import timedelta

from config.create_app import app

from modules.config.settings import TIME_NS


def generate_random_id(count: int = 32) -> str:
    """generate random string length in count."""
    if count < TIME_NS:
        return random.choices(string.ascii_lowercase + string.digits, k=count)

    return str(time.time_ns()) + random.choices(
        string.ascii_lowercase + string.digits, k=count - TIME_NS
    )


async def set_cache(key: str, value, ex: timedelta = None) -> bool:
    if not all((key, value)):
        return False

    params = {'name': 'blog.cache.' + key, 'value': value}
    if ex:
        params['ex'] = ex

    if isinstance(value, int | float | str):
        return await app.redis.set(**params)
    else:
        try:
            params['value'] = json.dumps(value)
            return await app.redis.set(**params)
        except json.JSONDecodeError:
            return False


async def get_cache(key: str) -> str:
    return await app.redis.get('blog.cache.' + key)


async def del_cache(key: str) -> str:
    return await app.redis.delete('blog.cache.' + key)
