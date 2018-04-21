from quiz_app_framework.data import BaseDatabase
from quiz_app_framework.models import Answer


class AnswerDatabase(BaseDatabase):

    def __init__(self):
        super().__init__(Answer)
