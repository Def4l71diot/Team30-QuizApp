from .base_dao import BaseDAO

from peewee import *


class User(BaseDAO):
    password_hash = CharField()
    salt = CharField()
