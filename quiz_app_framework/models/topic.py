from quiz_app_framework import BaseModel

from peewee import *


class Topic(BaseModel):
    name = CharField(unique=True)
