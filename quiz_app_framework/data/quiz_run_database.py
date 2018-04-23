from quiz_app_framework.data import BaseDatabase

from quiz_app_framework.models import QuizRun


class QuizRunDatabase(BaseDatabase):

    def __init__(self):
        super().__init__(QuizRun)
