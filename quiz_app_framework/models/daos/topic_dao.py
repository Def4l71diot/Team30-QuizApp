from quiz_app_framework.models.daos import BaseDAO

from peewee import *


class Topic(BaseDAO):
    name = CharField(unique=True)
