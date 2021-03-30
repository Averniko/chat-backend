from os import environ
from motor import motor_asyncio

DEBUG = environ.get('DEBUG', False)

HOST = environ.get('HOST', 'localhost')
PORT = environ.get('PORT', '8080')
SECRET_KEY = environ.get('SECRET_KEY', 'pass')
MONGO_HOST = environ.get('MONGO_HOST', 'mongodb://127.0.0.1:27017')
MONGO_DB_NAME = environ.get('MONGO_DB_NAME', 'chat')
MONGO_DB_USER = environ.get('MONGO_DB_USER', 'admin')
MONGO_DB_PASSWORD = environ.get('MONGO_DB_PASSWORD', 'pass')

MESSAGE_COLLECTION = 'messages'
USER_COLLECTION = 'users'

DB_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_HOST)
DB = DB_CLIENT[MONGO_DB_NAME]
