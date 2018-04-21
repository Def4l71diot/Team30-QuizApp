from peewee import fn

from quiz_app_framework.data import BaseDatabase
from quiz_app_framework.models import Question


class QuestionDatabase(BaseDatabase):
    def __init__(self):
        super().__init__(Question)
        self.dao_class = Question

    def delete(self, question):
        for answer in question.answers:
            answer.delete_instance()
        return super(QuestionDatabase, self).delete(question)

    def get_random_with_topic(self, topic, count):
        return self.dao_class.select().where(self.dao_class.topic == topic).order_by(fn.Random()).limit(count)
