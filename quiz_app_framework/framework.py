from quiz_app_framework.models import *
from quiz_app_framework.models.base_dao import DATABASE_PROXY


def setup(database):
    DATABASE_PROXY.initialize(database)
    with database:
        database.create_tables([Topic, Question, Answer, User])
