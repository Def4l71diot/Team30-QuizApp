from quiz_app_framework.models import Answer


class AnswerFactory:

    def create_answer(self, description, path_to_image=None):
        return Answer(description, path_to_image)
