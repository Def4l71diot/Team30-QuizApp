from quiz_app_framework.models import *
from quiz_app_framework.managers import *
from quiz_app_framework.models.base_dao import DATABASE_PROXY


class Framework:

    _instance = None

    def __init__(self, database):
        if isinstance(Framework._instance, Framework):
            raise Exception("Framework already initialized!")

        Framework._instance = self
        self._setup(database)

    def _setup(self, database):
        DATABASE_PROXY.initialize(database)
        with database:
            database.create_tables([Topic, Question, Answer, User, QuizRun, AnsweredQuestion])

        self.config_manager = ConfigManager()
        self.question_manager = QuestionManager()
        self.statistics_manager = StatisticsManager(question_database=self.question_manager._question_database)