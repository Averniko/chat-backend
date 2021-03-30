from src.chat.views import WebSocket, SendMessage, Messages
from src.auth.views import Login, Register, LogOut
from aiohttp.web import get, post

routes = [
    get('/api/ws', WebSocket, name='chat'),
    post('/api/login', Login, name='login'),
    post('/api/register', Register, name='register'),
    # post('/api/logout', LogOut, name='logout'),
    post('api/message/send', SendMessage, name='sendMessage'),
    get('/api/messages', Messages, name='messages')
]
