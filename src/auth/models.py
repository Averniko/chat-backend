from src.settings import USER_COLLECTION


class User:

    def __init__(self, db, data):
        self.db = db
        self.collection = self.db[USER_COLLECTION]
        self.login = data.get('login', None)
        self.password = data.get('password', None)

    async def find_user(self):
        if self.login is None:
            return None
        return await self.collection.find_one({'login': self.login})

    async def auth_user(self):
        result = await self.collection.find_one({'login': self.login, 'password': self.password})
        return result is not None

    async def create_user(self):
        user = await self.find_user()
        if user is not None:
            return user, False
        else:
            user = await self.collection.insert_one({'login': self.login, 'password': self.password})
            return user, True
