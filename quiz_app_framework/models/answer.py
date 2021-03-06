from .base_dao import BaseDAO

from quiz_app_framework.models import Question

from peewee import *


class Answer(BaseDAO):
    description = TextField()
    path_to_image = CharField(null=True, default=None)
    is_correct = BooleanField()
    question = ForeignKeyField(Question, backref='answers')
