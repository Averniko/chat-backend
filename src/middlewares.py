import jwt
from aiohttp import web

from src.auth import User
from .settings import *


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
        auth = request.headers.get('Authorization', None)
        if auth:
            token = auth.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            except jwt.exceptions.DecodeError:
                raise web.HTTPUnauthorized
            login = payload.get('login')
            user = await User(login=login).find_user()
            if user:
                request['user'] = user
                response = await handler(request)
                return response
        raise web.HTTPUnauthorized

    return middleware
