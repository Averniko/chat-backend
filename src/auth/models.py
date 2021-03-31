from src.settings import USER_COLLECTION, DB


class User:
    users = DB[USER_COLLECTION]

    def __init__(self, login: str, password: str = None):
        self._id = None
        self.login = login
        self.password = password
        self.contacts = []

    async def find_user(self):
        if self.login is None:
            return None
        result = await User.users.find_one({'login': self.login})
        if result:
            self._id = result['_id']
            self.contacts = result.get('contacts', [])
            return self
        else:
            return None

    async def auth_user(self):
        result = await User.users.find_one({'login': self.login, 'password': self.password})
        return bool(result)

    async def create(self):
        user = await self.find_user()
        if user:
            return user, False
        else:
            result = await User.users.insert_one({'login': self.login, 'password': self.password, 'contacts': []})
            self._id = result.inserted_id
            return self, True

    async def add_contact(self, contact):
        if contact.login in self.contacts:
            return False
        self.contacts.append(contact.login)
        result = await User.users.update_one({'login': self.login}, {'$set': {'contacts': self.contacts}})
        return bool(result)
