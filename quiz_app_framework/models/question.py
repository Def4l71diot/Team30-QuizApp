from .base_dao import BaseDAO

from quiz_app_framework.models import Topic

from peewee import *


class Question(BaseDAO):
    description = TextField()
    topic = ForeignKeyField(Topic, backref='questions')
    path_to_image = CharField(null=True, default=None)

    def __repr__(self):
        representation = "ID in database: " + str(self.id)
        representation += "\nDescription: " + self.description
        representation += "\nImage: " + str(self.path_to_image)
        representation += "\nTopic: " + self.topic.name
        representation += "\nAnswers:"
        for i, answer in enumerate(self.answers):
            representation += "\n\t" + str(i + 1) + ". " \
                              + answer.description + (" - correct answer" if answer.is_correct else "")
            representation += "\n\t\tImage: " + str(answer.path_to_image)

        return representation
