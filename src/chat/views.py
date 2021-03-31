from aiohttp import web, WSMsgType
from src.chat import Message
import json


class Messages(web.View):
    async def get(self):
        messages = Message().get_messages()
        return web.Response(content_type='application/json', text=json.dumps({'messages': messages}))


class SendMessage(web.View):
    async def post(self):
        data = await self.request.json()
        text = data.get('text', None)
        to_login = data.get('to', None)
        user = self.request.get('user')
        if text is None or to_login is None or user.login is None:
            return web.Response(status=400)
        message = await Message(text=text, from_login=user.login, to_login=to_login).save()

        for ws in self.request.app['websockets']:
            ws.send_str(json.dumps(
                {
                    'message': {
                        'from': user.login,
                        'text': message.text
                    }
                }))


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.tp == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()

        # self.request.app['websockets'].remove(ws)
        # for _ws in self.request.app['websockets']:
        #     _ws.send_str(f'{login} disconected')

        return ws
