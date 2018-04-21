from quiz_app_framework.models import User
from quiz_app_framework.data import BaseDatabase


class UserDatabase(BaseDatabase):

    def __init__(self):
        super().__init__(User)