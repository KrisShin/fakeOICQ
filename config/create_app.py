import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis import asyncio
from tortoise.contrib.fastapi import register_tortoise

from config.settings import BASE_DIR, DEBUG, HTTP_PORT, REDIS_URL, TORTOISE_ORM


def register_redis(app: FastAPI):
    """
    register redis to app
    """

    @app.lifespan("startup")
    async def startup_event():
        app.redis = await asyncio.from_url(
            REDIS_URL,
            decode_responses=True,
            encoding="utf8",
        )

    @app.lifespan("shutdown")
    async def shutdown_event():
        app.redis.close()


def init_db(app):
    """
    initialise database
    """
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=True,
    )


def create_app():
    if DEBUG:
        app = FastAPI()
    else:
        app = FastAPI(docs_url=None, redoc_url=None)
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "statics")),
        name="static",
    )
    origins = [
        "http://localhost",
        "http://localhost:" + HTTP_PORT,
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    return app


app = create_app()
