from quiz_app_framework.models.daos import Topic, Answer, Question
from quiz_app_framework.models.daos.base_dao import DATABASE_PROXY


def setup(database):
    DATABASE_PROXY.initialize(database)
    with database:
        database.create_tables([Topic, Answer, Question])
