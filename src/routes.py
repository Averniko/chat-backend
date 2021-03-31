from aiohttp.web import get, post

from src.auth.views import Login, Contacts, AddContact
from src.chat.views import WebSocket, SendMessage, Messages

routes = [
    get('/api/ws', WebSocket, name='chat'),
    post('/api/login', Login, name='login'),
    # post('/api/register', Register, name='register'),
    # post('/api/logout', LogOut, name='logout'),
    post('/api/message/send', SendMessage, name='sendMessage'),
    get('/api/messages', Messages, name='messages'),
    get('/api/dialogs', Contacts, name='contacts'),
    post('/api/contact/add', AddContact, name='addContact')
]
