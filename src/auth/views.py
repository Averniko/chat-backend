import json

import jwt
from aiohttp import web

from src.auth import User
from src.settings import *


class Login(web.View):
    async def post(self, **kwargs):
        data = await self.request.json()
        login = data.get('login')
        password = data.get('password')
        user = User(login=login, password=password)
        user, is_created = await user.create()
        if is_created:
            token = jwt.encode({"login": user.login}, SECRET_KEY, algorithm='HS256')
            return web.Response(content_type='application/json', text=json.dumps({'Token': token}))
        else:
            is_user_auth = await user.auth_user()
            if is_user_auth:
                token = jwt.encode({"login": user.login}, SECRET_KEY, algorithm='HS256')
                return web.Response(content_type='application/json', text=json.dumps({'Token': token}))
            else:
                return web.Response(status=401)


class Register(web.View):
    async def post(self, **kwargs):
        data = await self.request.json()
        user = User(data)
        user, is_created = await user.create_user()
        if is_created:
            token = jwt.encode({"login": user.login}, SECRET_KEY, algorithm='HS256')
            return web.Response(content_type='application/json', text=json.dumps({'Token': token}))
        else:
            return web.Response(content_type='application/json', text=json.dumps({'error': 'User already exists'}))


class LogOut(web.View):
    async def post(self, **kwargs):
        # TODO
        return web.Response(content_type='application/json', text=json.dumps({'error': 'Not implemented'}))
