from quiz_app_framework.data import QuestionDatabase, AnswerDatabase, TopicDatabase
import quiz_app_framework.constants as constants


class QuestionManager:

    def __init__(self,
                 question_database=QuestionDatabase(),
                 answer_database=AnswerDatabase(),
                 topic_database=TopicDatabase()):

        self.question_database = question_database
        self.answer_database = answer_database
        self.topic_database = topic_database

    def create_question(self, description, topic, answers, path_to_image=None):
        question = self.question_database.add(description=description,
                                              topic=topic,
                                              path_to_image=path_to_image)

        for answer in answers:
            if constants.ANSWER_PATH_TO_IMAGE_KEY not in answer:
                answer[constants.ANSWER_PATH_TO_IMAGE_KEY] = None

            if constants.ANSWER_IS_CORRECT_KEY not in answer:
                answer[constants.ANSWER_IS_CORRECT_KEY] = False

            self.answer_database.add(description=answer[constants.ANSWER_DESCRIPTION_KEY],
                                     path_to_image=answer[constants.ANSWER_PATH_TO_IMAGE_KEY],
                                     is_correct=answer[constants.ANSWER_IS_CORRECT_KEY],
                                     question=question)

        return question

    def update_question(self, question):
        return self.question_database.update(question)

    def delete_question(self, question):
        for answer in question.answers:
            self.answer_database.delete(answer)

        return self.question_database.delete(question)

    def get_all_questions(self):
        return self.question_database.get_all()

    def get_question(self, question_id):
        return self.question_database.get_by_id(question_id)

    def get_random_questions(self, number_of_questions, topic=None):
        if topic is None:
            return self.question_database.get_random(number_of_questions)
        else:
            return self.question_database.get_random_with_topic(topic, number_of_questions)

    def create_topic(self, topic_name):
        return self.topic_database.add(name=topic_name)

    def get_all_topics(self):
        return self.topic_database.get_all()

    def get_topic(self, topic_id):
        return self.topic_database.get_by_id(topic_id)
