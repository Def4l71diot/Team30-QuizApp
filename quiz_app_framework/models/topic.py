from .base_dao import BaseDAO

from peewee import *


class Topic(BaseDAO):
    name = CharField(unique=True)
