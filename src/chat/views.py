import jwt
from aiohttp import web, WSMsgType

from src.auth import User
from src.chat import Message
import json

from src.settings import SECRET_KEY


class Messages(web.View):
    async def get(self):
        query = self.request.query
        login_to = query.get('login')
        messages = await Message.get_dialog(first_login=self.request['user'].login, second_login=login_to)
        return web.Response(content_type='application/json', text=json.dumps({'messages': messages}, default=str))


class SendMessage(web.View):
    async def post(self):
        data = await self.request.json()
        text = data.get('text', None)
        to_login = data.get('to', None)
        user = self.request.get('user')
        if text is None or to_login is None or user.login is None:
            return web.Response(status=400)
        message = await Message(text=text, from_login=user.login, to_login=to_login).create()

        ws = self.request.app['websockets'].get(to_login)
        if ws:
            ws.send_str(json.dumps(
                {
                    'message': {
                        'from': user.login,
                        'text': message.text
                    }
                }))
        return web.Response(status=200)


class WebSocket(web.View):
    async def get(self):
        query = self.request.query
        token = query.get('token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        login = payload.get('login', None)
        user = await User(login=login).find_user()
        if user is None:
            web.Response(status=400)
        socket = self.request.app['websockets'].get(user.login, None)
        if socket:
            await socket.close()

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        self.request.app['websockets'][user.login] = ws

        async for msg in ws:
            if msg.tp == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                    self.request.app['websockets'][user.login] = None

        # self.request.app['websockets'].remove(ws)
        # for _ws in self.request.app['websockets']:
        #     _ws.send_str(f'{login} disconected')

        return ws
