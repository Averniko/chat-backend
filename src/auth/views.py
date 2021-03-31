import json

import jwt
from aiohttp import web

from src.auth import User
from src.chat import Message
from src.settings import *


class Contacts(web.View):
    async def get(self):
        user = self.request.get('user')
        contacts = user.contacts
        dialogs = []
        for contact in contacts:
            message = await Message.get_last_message(user.login, contact)
            dialog = {
                'login': contact,
                'lastMessage': message['text'] if message else None
            }
            dialogs.append(dialog)
        return web.Response(content_type='application/json', text=json.dumps({'dialogs': dialogs}, default=str))


class AddContact(web.View):
    async def post(self):
        data = await self.request.json()
        user = self.request.get('user')
        contact_login = data.get('login')
        contact = await User(login=contact_login).find_user()
        if contact:
            await user.add_contact(contact)
            await contact.add_contact(user)
            return web.Response(status=200)
        else:
            return web.Response(status=400)


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


class LogOut(web.View):
    async def post(self, **kwargs):
        # TODO
        return web.Response(content_type='application/json', text=json.dumps({'error': 'Not implemented'}))
