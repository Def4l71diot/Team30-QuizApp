from quiz_app_framework.data import QuestionDatabase, QuizRunDatabase, AnsweredQuestionDatabase


class StatisticsManager:

    def __init__(self,
                 question_database=QuestionDatabase(),
                 quiz_run_database=QuizRunDatabase(),
                 answered_question_database=AnsweredQuestionDatabase()):

        self._question_database = question_database
        self._quiz_run_database = quiz_run_database
        self._answered_question_database = answered_question_database

    def mark_question_answered_correctly(self, question):
        question.number_of_times_answered_correctly += 1

        self._question_database.update(question)

    def mark_question_answered_incorrectly(self, question):
        question.number_of_times_answered_incorrectly += 1

        self._question_database.update(question)

    def mark_question_skipped(self, question):
        question.number_of_times_skipped += 1

        self._question_database.update(question)

    def mark_question_was_asked(self, question):
        question.number_of_times_asked += 1

        self._question_database.update(question)

    def get_hardest_question(self):
        all_questions = self._question_database.get_all_asked_questions()
        if len(all_questions) == 0:
            return None

        hardest_question = all_questions[0]
        for question in all_questions:
            if question.percentage_answered_incorrectly > hardest_question:
                hardest_question = question

        return hardest_question

    def save_quiz_run(self, topic, student_school, student_year_group, questions_and_answers):

        quiz_run = self._quiz_run_database.add(student_year_group=student_year_group,
                                               student_school=student_school,
                                               topic=topic)

        for question in questions_and_answers:
            self._answered_question_database.add(question=question,
                                                 selected_answer=questions_and_answers[question],
                                                 from_quiz_run=quiz_run)

        return quiz_run

    def get_all_quiz_runs(self):
        return self._quiz_run_database.get_all()
