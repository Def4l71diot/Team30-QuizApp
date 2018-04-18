from quiz_app_framework import BaseModel, Question

from peewee import *


class Answer(BaseModel):
    description = TextField()
    pathToImage = CharField(null=True, default=None)
    question = ForeignKeyField(Question, backref='answers')
