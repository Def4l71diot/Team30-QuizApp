from quiz_app_framework.models import Answer


class AnswerFactory:

    def create_answer(self, description, is_correct=False, path_to_image=None):
        return Answer(description, is_correct, path_to_image)
