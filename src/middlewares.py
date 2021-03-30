from aiohttp import web
from .settings import *
import jwt
from src.auth import User


async def db_handler(app, handler):
    async def middleware(request):
        request.db = app.db
        response = await handler(request)
        return response

    return middleware


async def authorize(app, handler):
    async def middleware(request):
        if request.path.startswith(('/api/login', '/api/register', '/api/logout', '/api/ws')):
            response = await handler(request)
            return response
        # TODO
        auth = request.headers['Authorization']
        token = auth.split(' ')[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User(request.db, payload).find_user()
        if user:
            request.user = user
            return handler(request)
        else:
            raise web.HTTPUnauthorized

    return middleware
