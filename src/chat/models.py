from datetime import datetime
from src.settings import MESSAGE_COLLECTION


class Message:

    def __init__(self, db, user=None, text=None, **kwargs):
        self.collection = db[MESSAGE_COLLECTION]
        self.user = user
        self.text = text

    async def save(self, **kwargs):
        result = await self.collection.insert({'user': self.user, 'text': self.text, 'time': datetime.now()})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)
