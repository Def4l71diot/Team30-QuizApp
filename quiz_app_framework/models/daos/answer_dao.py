from quiz_app_framework.models.daos import BaseDAO, Question

from peewee import *


class Answer(BaseDAO):
    description = TextField()
    path_to_image = CharField(null=True, default=None)
    question = ForeignKeyField(Question, backref='answers')
    is_correct = BooleanField()
