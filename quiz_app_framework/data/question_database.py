from quiz_app_framework.data import BaseDatabase
from quiz_app_framework.models.daos import *


class QuestionDatabase(BaseDatabase):
    def __init__(self):
        super().__init__(Question)
        self.dao_class = Question

    def save(self, question_to_save):
        question = self.dao_class.create(
            description=question_to_save.description,
            topic=question_to_save.topic,
            path_to_image=question_to_save.path_to_image
        )

        for answer in question_to_save.answers:
            Answer.create(
                description=answer.description,
                path_to_image=answer.path_to_image,
                is_correct=answer.is_correct,
                question=question
            )

        return question

    def delete(self, question):
        for answer in question.answers:
            answer.delete_instance()
        return super(QuestionDatabase, self).delete(question)

    def save_topic(self, topic_to_save):
        return Topic.get_or_create(name=topic_to_save.name)

    def get_all_topics(self):
        return Topic.select()
