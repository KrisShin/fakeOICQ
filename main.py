import uvicorn
from config.create_app import create_app
from config.settings import HTTP_PORT

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=HTTP_PORT)
