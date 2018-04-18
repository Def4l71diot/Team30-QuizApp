from quiz_app_framework.models.daos import BaseDAO, Topic, Answer

from peewee import *


class Question(BaseDAO):
    description = TextField()
    topic = ForeignKeyField(Topic, backref='questions')
    path_to_image = CharField(null=True, default=None)
    correct_answer = ForeignKeyField(Answer)
