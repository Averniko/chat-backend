import asyncio
from aiohttp import web
from motor import motor_asyncio

from src.routes import routes
from src.middlewares import db_handler, authorize
from src.settings import *


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def init():
    app = web.Application(middlewares=[
        authorize,
        db_handler,
    ])
    app['websockets'] = []

    # routes
    app.add_routes(routes)

    # db
    app.client = motor_asyncio.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == '__main__':
    web.run_app(init(), host=HOST, port=PORT)
