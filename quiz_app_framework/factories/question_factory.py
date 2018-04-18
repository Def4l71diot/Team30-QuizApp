from quiz_app_framework.models import Question


class QuestionFactory:

    def create_question(self, description, topic, answers, path_to_image=None):
        return Question(description, topic, answers, path_to_image)
