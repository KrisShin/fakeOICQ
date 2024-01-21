from fastapi import FastAPI
from tortoise import Tortoise

from modules.common.test_apis import router as test_router

# from modules.common.apis import router as tag_router
# from modules.user.apis import router as user_router


def register_router(app: FastAPI):
    """
    register router to app
    """

    Tortoise.init_models(
        [
            'modules.common.models'
        ],
        'models',
    )

    app.include_router(
        test_router,
        tags=['test'],
        responses={404: {'description': 'Not Found'}},
        prefix="/api/test",
    )
    # app.include_router(
    #     tag_router,
    #     tags=['tag'],
    #     responses={404: {'description': 'Not Found'}},
    #     prefix="/api/tag",
    # )
    # app.include_router(
    #     user_router,
    #     tags=['user'],
    #     responses={404: {'description': 'Not Found'}},
    #     prefix='/api/user',
    # )
