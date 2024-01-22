from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis import asyncio
from tortoise.contrib.fastapi import register_tortoise

from config.settings import BASE_DIR, DEBUG, HTTP_PORT, REDIS_URL, TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.redis = await asyncio.from_url(
        REDIS_URL,
        decode_responses=True,
        encoding="utf8",
    )
    yield
    app.redis.close()


# def register_redis(app: FastAPI):
#     """
#     register redis to app
#     """

#     @app.on_event("startup")
#     async def startup_event():
#         app.redis = await asyncio.from_url(
#             REDIS_URL,
#             decode_responses=True,
#             encoding="utf8",
#         )

#     @app.lifespan("shutdown")
#     async def shutdown_event():
#         app.redis.close()


# def init_db(app):
#     """
#     initialise database
#     """
#     register_tortoise(
#         app,
#         config=TORTOISE_ORM,
#         add_exception_handlers=True,
#     )


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
        f"http://localhost:{HTTP_PORT}",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=True,
    )

    return app


app = create_app()
