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

    def get_all(self, and_deleted=False):
        if and_deleted:
            return super(QuestionDatabase, self).get_all()
        else:
            return self.dao_class.select().where(self.dao_class.is_deleted == False)

    def get_random(self, number_of_records):
        return self.dao_class\
            .select()\
            .where(self.dao_class.is_deleted == False)\
            .order_by(self._db_random_func())\
            .limit(number_of_records)

    def get_random_with_topic(self, topic, count):
        return self.dao_class\
            .select()\
            .where((self.dao_class.topic == topic) & (self.dao_class.is_deleted == False))\
            .order_by(self._db_random_func())\
            .limit(count)
