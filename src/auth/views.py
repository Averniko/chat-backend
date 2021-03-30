import json
from aiohttp import web
from src.auth import User
import jwt
from src.settings import *


class Login(web.View):

    async def post(self, **kwargs):
        data = await self.request.json()
        user = User(self.request.db, data)
        is_user_auth = await user.auth_user()
        if is_user_auth:
            token = jwt.encode({"login": user.login}, SECRET_KEY, algorithm='HS256')
            return web.Response(content_type='application/json', text=json.dumps({'Token': token}))
        else:
            return web.Response(status=401)


class Register(web.View):

    async def post(self, **kwargs):
        data = await self.request.json()
        user = User(self.request.db, data)
        user, is_created = await user.create_user()
        if is_created:
            token = jwt.encode({"login": user.login}, SECRET_KEY, algorithm='HS256')
            return web.Response(content_type='application/json', text=json.dumps({'Token': token}))
        else:
            return web.Response(content_type='application/json', text=json.dumps({'error': 'User already exist'}))


class LogOut(web.View):

    async def post(self, **kwargs):
        # TODO
        return web.Response(content_type='application/json', text=json.dumps({'error': 'Not implemented'}))
