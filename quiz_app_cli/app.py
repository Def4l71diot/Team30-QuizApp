import quiz_app_framework as qaf
from quiz_app_cli.providers import *


class App:
    def __init__(self,
                 config_manager: qaf.ConfigManager,
                 question_manager: qaf.QuestionManager,
                 statistics_manager: qaf.StatisticsManager,
                 reader: ConsoleReaderProvider,
                 writer: ConsoleWriterProvider):
        self._config_manager = config_manager
        self._question_manager = question_manager
        self._statistics_manager = statistics_manager
        self._reader = reader
        self._writer = writer

    def run(self):
        try:
            if self._config_manager.is_first_launch:
                password = self._reader.read_input_hidden("Please enter a password for the admin account: ")
                is_admin_created = self._config_manager.register_admin(password)
                if not is_admin_created:
                    raise Exception("And error occurred while creating admin account!")

            password = self._reader.read_input_hidden("Log in: ")

            if not self._config_manager.login_admin(password):
                raise Exception("Wrong password!")

        except Exception as e:
            self._writer.write(e)
            return

        while True:
            try:
                command = self._reader.read_input("Please enter a command: ")
                if command == "questions":
                    self._login_guard()
                    self._list_all_questions()
                elif command == "topics":
                    self._login_guard()
                    self._list_all_topics()
                elif command == "createTopic":
                    self._login_guard()
                    self._create_topic()
                elif command == "createQuestion":
                    self._login_guard()
                    self._create_question()
                elif command == "deleteQuestion":
                    self._login_guard()
                    self._delete_question()
                elif command == "editQuestion":
                    self._login_guard()
                    self._edit_question()
                elif command == "help":
                    self._show_help()
                elif command == "exit":
                    break
                else:
                    self._writer.write("Invalid command!")
            except ValueError:
                self._writer.write("Please enter a valid value!")
            except IndexError:
                self._writer.write("Invalid item selected!")
            except Exception as e:
                self._writer.write(e)

    def _list_all_questions(self):
        questions = self._question_manager.get_all_questions()
        self._writer.write()
        self._print_questions(questions)

    def _list_all_topics(self):
        topics = self._question_manager.get_all_topics()
        for index, topic in enumerate(topics):
            self._writer.write(str(index + 1) + ". " + topic.name)

    def _create_topic(self):
        name = self._reader.read_input("Please enter topic name: ")
        self._question_manager.create_topic(name)

    def _create_question(self):
        topics = self._question_manager.get_all_topics()
        if len(topics) == 0:
            self._writer.write("No topics available! Please create one using 'createTopic'")
            return

        for index, topic in enumerate(topics):
            self._writer.write(str(index + 1) + ". " + topic.name)

        question_topic_position = int(self._reader.read_input("Select question topic: "))
        topic = topics[question_topic_position - 1]

        description = self._reader.read_input("Enter question description: ")

        answers = [{}, {}, {}, {}]

        self._writer.write("Please enter 4 answers:")
        for i in range(0, 4):
            answer_description = self._reader.read_input("Answer " + str(i + 1) + ": ")
            answers[i][qaf.ANSWER_DESCRIPTION_KEY] = answer_description

        correct_answer_index = int(
            self._reader.read_input("Select the correct answer(Enter a value between 1 and 4): "))
        answers[correct_answer_index - 1][qaf.ANSWER_IS_CORRECT_KEY] = True

        question = self._question_manager.create_question(description, topic, answers)

        self._writer.write("Question created successfully!")
        self._writer.write_separator()
        self._writer.write(question)

    def _delete_question(self):
        question_id = int(self._reader.read_input("Enter the ID of the question to delete: "))
        question_to_delete = self._question_manager.get_question(question_id)
        if question_to_delete is None:
            raise Exception("Question with ID " + str(question_id) + " does not exist!")

        affected_records = self._question_manager.delete_question(question_to_delete)
        self._writer.write("Affected records: " + str(affected_records))

    def _edit_question(self):
        question_id = int(self._reader.read_input("Enter the ID of the question to edit: "))
        question_to_edit = self._question_manager.get_question(question_id)
        if question_to_edit is None:
            raise Exception("Question with ID " + str(question_id) + " does not exist!")

        self._writer.write("Edit question: " + '"' + question_to_edit.description + '"')
        self._writer.write()
        topics = self._question_manager.get_all_topics()
        for index, topic in enumerate(topics):
            self._writer.write(str(index + 1) + ". " + topic.name)

        index_of_question_topic = list(topics).index(question_to_edit.topic)
        new_topic_position = int(self._reader.read_input("Select question topic: ",
                                                         value_for_editing=str(index_of_question_topic + 1)))

        question_to_edit.topic = topics[new_topic_position - 1]

        new_description = self._reader.read_input("Edit description: ",
                                                  value_for_editing=question_to_edit.description)
        if new_description:
            question_to_edit.description = new_description

        editable_answers = [self._question_manager.get_answer(x.id) for x in question_to_edit.answers]

        index_of_correct_answer = None
        for index, answer in enumerate(editable_answers):
            if answer.is_correct:
                index_of_correct_answer = index

            answer_edit_prompt = "Edit answer " + str(index + 1) + (" (correct): " if answer.is_correct else ": ")
            answer_new_description = self._reader.read_input(answer_edit_prompt, value_for_editing=answer.description)

            if answer_new_description:
                answer.description = answer_new_description

        new_correct_answer_prompt = "Select the correct answer(Enter a value between 1 and " \
                                    + str(len(editable_answers)) + "): "
        position_of_new_correct_answer = int(self._reader.read_input(new_correct_answer_prompt,
                                                                     str(index_of_correct_answer + 1)))

        editable_answers[index_of_correct_answer].is_correct = False
        editable_answers[position_of_new_correct_answer - 1].is_correct = True

        for edited_answer in editable_answers:
            self._question_manager.update_answer(edited_answer)

        self._question_manager.update_question(question_to_edit)
        self._writer.write("Question updated successfully!")

    def _show_help(self):
        self._writer.write("questions - display all questions")
        self._writer.write("topics - display all topics")
        self._writer.write("createTopic - create a topic")
        self._writer.write("createQuestion - create a question")
        self._writer.write("delete - delete a question")
        self._writer.write("exit - exit the program")

    def _login_guard(self):
        if not self._config_manager.is_admin_logged_in:
            raise Exception("You must be logged in order to perform this action!")

    def _print_questions(self, questions):
        self._writer.write_separator()
        for question in questions:
            self._writer.write(question)
            self._writer.write_separator()
