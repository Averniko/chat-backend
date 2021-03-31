from aiohttp import web
from src.middlewares import db_handler, authorize
from src.routes import routes
from src.settings import *
from aiohttp_middlewares import cors_middleware


async def on_shutdown(app):
    for ws in app['websockets'].values():
        await ws.close(code=1001, message='Server shutdown')


async def init():
    app = web.Application(middlewares=[
        cors_middleware(allow_all=True),
        authorize,
        db_handler,
    ])
    app['websockets'] = {}

    # routes
    app.add_routes(routes)

    # db
    app.client = DB_CLIENT
    app.db = DB

    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == '__main__':
    web.run_app(init(), host=HOST, port=PORT)
