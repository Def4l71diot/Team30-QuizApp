from .base_dao import BaseDAO

from quiz_app_framework.models import Topic

from peewee import *


class QuizRun(BaseDAO):
    student_year_group = CharField()
    student_school = CharField()
    topic = ForeignKeyField(Topic, null=True)

    def __repr__(self):
        representation = "Student school: " + self.student_school
        representation += "\nStudent year group: " + self.student_year_group
        representation += "\nTopic: " + ("All" if self.topic is None else self.topic.name)
        representation += "\nQuestions and answers: "
        for answered_question in self.questions_and_answers:
            representation += "\n\tQuestion: " + answered_question.question.description
            if answered_question.selected_answer is not None:
                representation += "\n\t\tAnswer: " + answered_question.selected_answer.description
                representation += " - correct" if answered_question.selected_answer.is_correct else ""
            else:
                representation += "\n\t\tAnswer: None"

        return representation
