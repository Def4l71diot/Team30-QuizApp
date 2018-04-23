from .base_dao import BaseDAO

from quiz_app_framework.models import Topic

from peewee import *


class Question(BaseDAO):
    description = TextField()
    topic = ForeignKeyField(Topic, backref='questions')
    path_to_image = CharField(null=True, default=None)
    number_of_times_answered_correctly = BigIntegerField(default=0)
    number_of_times_answered_incorrectly = BigIntegerField(default=0)
    number_of_times_skipped = BigIntegerField(default=0)
    number_of_times_asked = BigIntegerField(default=0)
    is_deleted = BooleanField(default=False)

    @property
    def percentage_answered_correctly(self):
        if self.number_of_times_asked == 0:
            return 0

        return (self.number_of_times_answered_correctly / self.number_of_times_asked) * 100

    @property
    def percentage_answered_incorrectly(self):
        if self.number_of_times_asked == 0:
            return 0

        return (self.number_of_times_answered_incorrectly / self.number_of_times_asked) * 100

    @property
    def percentage_skipped(self):
        if self.number_of_times_asked == 0:
            return 0

        return (self.number_of_times_skipped / self.number_of_times_asked) * 100

    def __repr__(self):
        representation = "This question is marked as DELETED\n" if self.is_deleted else ""
        representation += "ID in database: " + str(self.id)
        representation += "\nDescription: " + self.description
        representation += "\nImage: " + str(self.path_to_image)
        representation += "\nTopic: " + self.topic.name
        representation += "\nAnswers:"
        for i, answer in enumerate(self.answers):
            representation += "\n\t" + str(i + 1) + ". " \
                              + answer.description + (" - correct answer" if answer.is_correct else "")
            representation += "\n\t\tImage: " + str(answer.path_to_image)
        representation += "\nStatistics:\nTimes asked: " + str(self.number_of_times_asked)
        representation += "\nTimes answered correctly: " + str(self.number_of_times_answered_correctly) \
                          + " - " + str(self.percentage_answered_correctly) + " %"
        representation += "\nTimes answered incorrectly: " + str(self.number_of_times_answered_incorrectly) \
                          + " - " + str(self.percentage_answered_incorrectly) + " %"
        representation += "\nTimes skipped: " + str(self.number_of_times_skipped) \
                          + " - " + str(self.percentage_skipped) + " %"

        return representation
