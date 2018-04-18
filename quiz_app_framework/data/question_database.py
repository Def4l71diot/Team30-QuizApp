from quiz_app_framework.data import BaseDatabase
from quiz_app_framework.models.daos import *
import quiz_app_framework.models as m


class QuestionDatabase(BaseDatabase):
    def __init__(self):
        super().__init__(Question)
        self.dao_class = Question

    def save(self, object_to_save: m.Question):
        question = self.dao_class.create(
            description=object_to_save.description,
            topic=object_to_save.topic,
            path_to_image=object_to_save.path_to_image
        )

        for answer in object_to_save.answers:
            Answer.create(
                description=answer.description,
                path_to_image=answer.path_to_image,
                is_correct=answer.is_correct,
                question=question
            )

        return question

    def save_topic(self, topic_to_save: m.Topic):
        return Topic.get_or_create(name=topic_to_save.name)

    def get_all_topics(self):
        return Topic.select()
