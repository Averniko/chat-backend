from src.settings import USER_COLLECTION, DB


class User:
    users = DB[USER_COLLECTION]

    def __init__(self, data):
        self.login = data.get('login', None)
        self.password = data.get('password', None)

    async def find_user(self):
        if self.login is None:
            return None
        return await User.users.find_one({'login': self.login})

    async def auth_user(self):
        result = await User.users.find_one({'login': self.login, 'password': self.password})
        return bool(result)

    async def create_user(self):
        user = await self.find_user()
        if user:
            return user, False
        else:
            user = await User.users.insert_one({'login': self.login, 'password': self.password})
            return user, True
