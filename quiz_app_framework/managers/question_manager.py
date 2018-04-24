from quiz_app_framework.data import QuestionDatabase, AnswerDatabase, TopicDatabase
import quiz_app_framework.constants as constants


class QuestionManager:

    def __init__(self,
                 question_database=QuestionDatabase(),
                 answer_database=AnswerDatabase(),
                 topic_database=TopicDatabase()):

        self._question_database = question_database
        self._answer_database = answer_database
        self._topic_database = topic_database

    def create_question(self, description, topic, answers, path_to_image=None):
        question = self._question_database.add(description=description,
                                               topic=topic,
                                               path_to_image=path_to_image)

        for answer in answers:
            if constants.ANSWER_PATH_TO_IMAGE_KEY not in answer:
                answer[constants.ANSWER_PATH_TO_IMAGE_KEY] = None

            if constants.ANSWER_IS_CORRECT_KEY not in answer:
                answer[constants.ANSWER_IS_CORRECT_KEY] = False

            self._answer_database.add(description=answer[constants.ANSWER_DESCRIPTION_KEY],
                                      path_to_image=answer[constants.ANSWER_PATH_TO_IMAGE_KEY],
                                      is_correct=answer[constants.ANSWER_IS_CORRECT_KEY],
                                      question=question)

        return question

    def update_question(self, question):
        return self._question_database.update(question)

    def update_answer(self, answer):
        return self._answer_database.update(answer)

    def delete_question(self, question):
        question.is_deleted = True

        return self.update_question(question)

    def get_all_questions(self, and_deleted=False):
        return self._question_database.get_all(and_deleted=and_deleted)

    def get_question_count(self):
        return self._question_database.get_number_of_records()

    def get_question(self, question_id):
        return self._question_database.get_by_id(question_id)

    def get_answer(self, answer_id):
        return self._answer_database.get_by_id(answer_id)

    def get_random_questions(self, number_of_questions, topic=None):
        if topic is None:
            return self._question_database.get_random(number_of_questions)
        else:
            return self._question_database.get_random_with_topic(topic, number_of_questions)

    def create_topic(self, topic_name):
        return self._topic_database.add(name=topic_name)

    def get_all_topics(self):
        return self._topic_database.get_all()

    def get_topic(self, topic_id):
        return self._topic_database.get_by_id(topic_id)
