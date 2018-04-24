import quiz_app_framework as qaf


class App:
    def __init__(self,
                 config_manager,
                 question_manager,
                 statistics_manager,
                 reader,
                 writer):
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
        except KeyboardInterrupt:
            self._writer.write()
            self._writer.write("Thank you for using the quiz app!")
            return

        self._writer.write("Logged in successfully!")
        self._writer.write()
        self._show_help()
        self._writer.write()

        while True:
            try:
                command = self._reader.read_input("Please enter a command: ")
                if command == "questions":
                    self._login_guard()
                    self._list_all_questions()
                elif command == "hardestQuestion":
                    self._writer.write(str(self._statistics_manager.get_hardest_question()))
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
                elif command == "setupQuiz":
                    self._login_guard()
                    try:
                        self._setup_quiz()
                    except KeyboardInterrupt:
                        self._writer.write()
                elif command == "quizRuns":
                    self._login_guard()
                    self._list_quiz_runs()
                elif command == "login":
                    self._login()
                elif command == "help":
                    self._show_help()
                elif command == "exit":
                    self._login_guard()
                    break
                else:
                    self._writer.write("Invalid command!")
            except ValueError:
                self._writer.write("Please enter a valid value!")
            except IndexError:
                self._writer.write("Invalid item selected!")
            except KeyboardInterrupt:
                self._writer.write()
                if not self._config_manager.is_admin_logged_in:
                    self._writer.write("You must be logged in in order to close the app!")
                    continue
                self._writer.write("Thank you for using the quiz app!")
                return
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
        self._writer.write("hardestQuestion - the hardest question")
        self._writer.write("topics - display all topics")
        self._writer.write("createTopic - create a topic")
        self._writer.write("createQuestion - create a question")
        self._writer.write("deleteQuestion - delete a question")
        self._writer.write("editQuestion - edit an existing question")
        self._writer.write("setupQuiz - setup and run the quiz")
        self._writer.write("quizRuns - get all quiz runs")
        self._writer.write("exit - exit the program")
        self._writer.write("login - login to admin account(in case you get logged out)")
        self._writer.write("help - display this message")

    def _login_guard(self):
        if not self._config_manager.is_admin_logged_in:
            raise Exception("You must be logged in order to perform this action!")

    def _login(self):
        if self._config_manager.is_admin_logged_in:
            raise Exception("You are already logged in")

        password = self._reader.read_input_hidden("Enter admin password: ")
        if not self._config_manager.login_admin(password):
            raise Exception("Wrong password!")

        self._writer.write("Logged in successfully!")

    def _print_questions(self, questions):
        self._writer.write_separator()
        for question in questions:
            self._writer.write(question)
            self._writer.write_separator()

    def _setup_quiz(self):
        if self._question_manager.get_question_count() == 0:
            raise Exception("No questions found! You must create some!")

        self._writer.write("Okay, lets setup the quiz.")

        self._writer.write()
        self._writer.write("Do you wish to choose a topic?")
        self._writer.write("0. No Topic")
        topics = self._question_manager.get_all_topics()
        self._list_all_topics()
        self._writer.write()

        question_topic_position = self._reader.read_input("Please select a topic: ")
        while True:
            try:
                int(question_topic_position)
                break
            except ValueError:
                if question_topic_position == "restart":
                    self._writer.write("restarting quiz")
                    self._writer.write()
                    self._setup_quiz()
                else:
                    self._writer.write("Invalid input")
                    question_topic_position = self._reader.read_input("Please select a topic: ")

        while (int(question_topic_position) < 0) or (int(question_topic_position) > len(topics)):
            self._writer.write("Invalid input")
            question_topic_position = self._reader.read_input("Please select a topic: ")

        if int(question_topic_position) == 0:
            topic = None

        else:
            topic = topics[int(question_topic_position) - 1]

        self._writer.write()
        number_of_questions = int(self._reader.read_input("How many questions to ask each visitor?: "))
        self._writer.write()

        schools = self._get_items("school")

        year_groups = self._get_items("year group")
        self._config_manager.logout_admin()
        self._take_quiz(number_of_questions, schools, year_groups, topic)

    def _get_items(self, item_name):
        items = []
        while True:
            items.append(self._reader.read_input("Please enter {}: ".format(item_name)))

            while True:
                command = self._reader.read_input("Add another {}?(y/n): ".format(item_name)).lower()
                if command == "y":
                    break
                elif command == "n":
                    return items
                else:
                    self._writer.write("Invalid Input!")

    def _take_quiz(self, number_of_questions, schools, year_groups, topic=None):
        try:
            while True:
                self._writer.clear()
                questions = self._question_manager.get_random_questions(number_of_questions, topic=topic)
                number_of_questions = len(questions)
                self._writer.write("Schools: ")
                for index, school in enumerate(schools):
                    self._writer.write(str(index + 1) + ". " + school)

                while True:
                    try:
                        school_position_raw = self._reader.read_input(
                            "What school do you attend? Pick from the list above: ")
                        school_position = int(school_position_raw)
                    except ValueError:
                        self._writer.write("Please enter a valid position!")
                        continue

                    if 1 <= school_position <= len(schools):
                        break
                    else:
                        self._writer.write("Invalid input!")

                student_school = schools[school_position - 1]

                self._writer.write("Year groups: ")
                for index, year_group in enumerate(year_groups):
                    self._writer.write(str(index + 1) + ". " + year_group)

                while True:
                    try:
                        year_group_position_raw = \
                            self._reader.read_input("What Year Group are you in? Pick from the list above: ")
                        year_group_position = int(year_group_position_raw)
                    except ValueError:
                        self._writer.write("Please enter a valid position!")
                        continue
                    if 1 <= year_group_position <= len(year_groups):
                        break
                    else:
                        self._writer.write("Invalid Input!")

                year_group = year_groups[year_group_position - 1]
                score = []
                i = 0
                questions_and_answers = {}
                while i < number_of_questions:
                    self._writer.write()
                    [answered_correctly, selected_answer] = self._ask_question(questions[i],
                                                                               number_of_questions,
                                                                               schools,
                                                                               year_groups,
                                                                               topic)
                    if not answered_correctly:
                        score.append(0)
                    else:
                        score.append(1)
                    questions_and_answers[questions[i]] = selected_answer
                    i += 1

                self._display_quiz_score(score, number_of_questions)
                self._statistics_manager.save_quiz_run(topic=topic,
                                                       student_school=student_school,
                                                       student_year_group=year_group,
                                                       questions_and_answers=questions_and_answers)
                self._reader.read_input("Resetting quiz. Press enter to continue...")
        except KeyboardInterrupt:
            self._writer.write()
            password = self._reader.read_input_hidden("Enter admin password: ")
            if self._config_manager.login_admin(password):
                return
            else:
                self._writer.write("Wrong password!")
                self._reader.read_input("Resetting quiz. Press enter to continue...")
                self._writer.clear()

    def _ask_question(self, question, number_of_questions, schools, year_groups, topic):
        self._writer.write("To restart the quiz at anytime type 'restart'")
        self._writer.write()
        skip = False
        skipped = False
        correct = False
        [correct_answer, correct_answer_description] = self._quiz_display_question(question)

        chosen_answer = self._reader.read_input("Please choose an answer, or type 'skip': ")

        if chosen_answer == "restart":
            self._writer.write("restarting quiz")
            self._writer.write()
            self._take_quiz(number_of_questions, schools, year_groups, topic)
        if chosen_answer == "skip":
            self._writer.write("skipping question")
            self._writer.write()
            self._statistics_manager.mark_question_skipped(question)
            skip = True
            skipped = True

        if not skip:
            while True:
                try:
                    int(chosen_answer)
                    break
                except ValueError:
                    if chosen_answer == "skip":
                        self._writer.write("skipping question")
                        self._writer.write()
                        correct = False
                        self._statistics_manager.mark_question_skipped(question)
                        skip = True
                        break
                    else:
                        self._writer.write("Invalid input. Please ensure you input a number.")
                        chosen_answer = self._reader.read_input("Please choose an answer: ")
        while not skip:
            while int(chosen_answer) > 4 or int(chosen_answer) < 1:
                self._writer.write("Invalid choice")
                chosen_answer = self._reader.read_input("Please choose an answer: ")

            if int(chosen_answer) == correct_answer:
                self._writer.write()
                self._writer.write("--Correct--")
                self._writer.write()
                correct = True
                self._statistics_manager.mark_question_answered_correctly(question)
            else:
                self._writer.write()
                self._writer.write("--Incorrect--")
                self._writer.write("Correct answer was " + correct_answer_description)
                self._writer.write()
                correct = False
                self._statistics_manager.mark_question_answered_incorrectly(question)
            skip = True

        if not skipped:
            return correct, question.answers[int(chosen_answer) - 1]
        else:
            return correct, None

    def _quiz_display_question(self, question):
        self._writer.write("Question: " + question.description)
        self._statistics_manager.mark_question_was_asked(question)

        correct_answer = None
        correct_answer_description = None
        for i, answer in enumerate(question.answers):
            if answer.is_correct:
                correct_answer = i + 1
                correct_answer_description = answer.description

            self._writer.write("Answer " + str(i + 1) + ". " + answer.description)

        return correct_answer, correct_answer_description

    def _display_quiz_score(self, score, number_of_questions):
        total_score = sum(score)
        self._writer.write("You scored " + str(total_score) + " out of " + str(number_of_questions))
        self._writer.write("Percentage: " + str(round((total_score / number_of_questions) * 100)) + "%")

    def _list_quiz_runs(self):
        quiz_runs = self._statistics_manager.get_all_quiz_runs()
        self._writer.write()
        for quiz_run in quiz_runs:
            self._writer.write(quiz_run)
            self._writer.write_separator()
