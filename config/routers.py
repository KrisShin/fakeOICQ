from fastapi import FastAPI
from tortoise import Tortoise

from modules.user.contact_apis import router as contact_router
from modules.user.user_apis import router as user_router
from modules.communication.apis import router as communication_router
from modules.common.apis import router as common_router


# from modules.common.test_apis import router as test_router


def register_router(app: FastAPI):
    """
    register router to app
    """

    Tortoise.init_models(
        [
            'modules.common.models',
            'modules.user.models',
            'modules.communication.models',
        ],
        'models',
    )

    # app.include_router(
    #     test_router,
    #     tags=['test'],
    #     responses={404: {'description': 'Not Found'}},
    #     prefix="/api/test",
    # )
    # app.include_router(
    #     tag_router,
    #     tags=['tag'],
    #     responses={404: {'description': 'Not Found'}},
    #     prefix="/api/tag",
    # )
    app.include_router(
        common_router,
        tags=['common'],
        responses={404: {'description': 'Not Found'}},
        prefix='/api/common',
    )
    app.include_router(
        user_router,
        tags=['user'],
        responses={404: {'description': 'Not Found'}},
        prefix='/api/user',
    )
    app.include_router(
        contact_router,
        tags=['contact'],
        responses={404: {'description': 'Not Found'}},
        prefix='/api/contact',
    )
    app.include_router(
        communication_router,
        tags=['communication'],
        responses={404: {'description': 'Not Found'}},
        prefix='/api/communication',
    )
