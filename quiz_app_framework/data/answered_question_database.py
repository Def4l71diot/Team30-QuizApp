from quiz_app_framework.data import BaseDatabase

from quiz_app_framework.models import AnsweredQuestion


class AnsweredQuestionDatabase(BaseDatabase):

    def __init__(self):
        super().__init__(AnsweredQuestion)
