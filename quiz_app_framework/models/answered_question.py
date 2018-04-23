from .base_dao import BaseDAO

from quiz_app_framework.models import Question, Answer, QuizRun

from peewee import *


class AnsweredQuestion(BaseDAO):
    question = ForeignKeyField(Question)
    selected_answer = ForeignKeyField(Answer, null=True, default=None)
    from_quiz_run = ForeignKeyField(QuizRun, backref='questions_and_answers')
