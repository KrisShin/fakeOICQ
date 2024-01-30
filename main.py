import uvicorn

from config.create_app import app
from config.routers import register_router
from config.settings import HTTP_PORT

register_router(app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=HTTP_PORT)
