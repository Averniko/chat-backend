from datetime import datetime

from src.settings import MESSAGE_COLLECTION, DB


class Message:
    messages = DB[MESSAGE_COLLECTION]

    def __init__(self, from_login=None, to_login=None, text=None, **kwargs):
        self.from_login = from_login
        self.to_login = to_login
        self.text = text

    async def create(self, **kwargs):
        result = await Message.messages.insert_one({
            'from': self.from_login,
            'to': self.to_login,
            'text': self.text,
            'time': datetime.now()
        })
        return result

    async def get_messages(self):
        messages = self.messages.find({}).sort([('time', 1)])
        return await messages.to_list(length=None)

    @staticmethod
    async def get_dialog(first_login, second_login):
        messages = Message.messages.find({'from': first_login, 'to': second_login},
                                         {'from': second_login, 'to': first_login}).sort([('time', 1)])
        return await messages.to_list(length=None)