import os
from typing import Type

from environ import Env
from tortoise.models import Model

env = Env(DEBUG=(bool, False))

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DEBUG")

TIME_NS = 16

PG_HOST = env('PG_HOST')
PG_PORT = env('PG_PORT')
PG_USER = env('PG_USER')
PG_PASS = env('PG_PASS')
PG_DB = env('PG_DB')
DB_URL = f"postgres://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_USER = env('REDIS_USER')
REDIS_PASS = env('REDIS_PASS')
REDIS_DB = env('REDIS_DB')
REDIS_URL = f"redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = env('SECRET_KEY', default='secret')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

HTTP_ADDR = 'http://localhost'
HTTP_PORT = 26798
HTTP_SITE = f'{HTTP_ADDR}:{HTTP_PORT}'
DEFAULT_AVATAR_PATH = f'/static/avatar'


class Router:
    def db_for_read(self, model: Type[Model]):
        return "slave"

    def db_for_write(self, model: Type[Model]):
        return "master"


TORTOISE_ORM = {
    "connections": {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': PG_HOST,
                'port': PG_PORT,
                'user': PG_USER,
                'password': PG_PASS,
                'database': PG_DB,
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                'aerich.models',
                'modules.common.models',
                'modules.user.models',
                'modules.communication.models',
            ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC",
}
