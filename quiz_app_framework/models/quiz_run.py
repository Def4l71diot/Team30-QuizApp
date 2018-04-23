from .base_dao import BaseDAO

from quiz_app_framework.models import Topic

from peewee import *


class QuizRun(BaseDAO):
    student_year_group = CharField()
    student_school = CharField()
    topic = ForeignKeyField(Topic)
