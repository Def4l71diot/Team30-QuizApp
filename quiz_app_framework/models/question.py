from quiz_app_framework import BaseModel, Topic, Answer

from peewee import *


class Question(BaseModel):
    description = TextField()
    topic = ForeignKeyField(Topic, backref='questions')
    pathToImage = CharField(null=True, default=None)
    correctAnswer = ForeignKeyField(Answer)