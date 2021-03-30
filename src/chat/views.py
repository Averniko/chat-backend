from aiohttp import web, WSMsgType
from src.chat import Message
import json


class Messages(web.View):
    async def get(self):
        messages = Message(self.request.db).get_messages()
        return web.Response(content_type='application/json', text=json.dumps({'messages': messages}))


class SendMessage(web.View):
    async def post(self):
        data = await self.request.json()
        text = data.get('text')
        user = self.request.user
        message = await Message(self.request.db, text=text, user=user).save()

        for ws in self.request.app['websockets']:
            ws.send_str(json.dumps(
                {
                    'message': {
                        'user': user.login,
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
