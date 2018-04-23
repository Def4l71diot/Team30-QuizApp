import quiz_app_framework as qaf

from peewee import SqliteDatabase
import getpass
import uuid
import random

database = SqliteDatabase("quiz_app.db")

framework = qaf.Framework(database)

question_manager = framework.question_manager

config_manager = framework.config_manager

statistics_manager = framework.statistics_manager


def run():
    try:
        if config_manager.is_first_launch:
            password = getpass.getpass("Please enter a password for the admin account: ")
            is_admin_created = config_manager.register_admin(password)
            if not is_admin_created:
                raise Exception("And error occurred while creating admin account!")

        password = getpass.getpass("Log in: ")

        if not config_manager.login_admin(password):
            raise Exception("Wrong password!")

    except Exception as e:
        print(e)
        return

    while True:
        try:
            command = input("Please enter a command: ")
            if command == "questions":
                login_guard()
                list_all_questions()
            elif command == "topics":
                login_guard()
                list_all_topics()
            elif command == "createTopic":
                login_guard()
                create_topic()
            elif command == "createQuestion":
                login_guard()
                create_question()
            elif command == "delete":
                login_guard()
                delete_question()
            elif command == "random":
                login_guard()
                list_random()
            elif command == "quiz_run":
                login_guard()
                example_save_quiz_run_to_statistics()
            elif command == "help":
                show_help()
            elif command == "exit":
                break
            else:
                print("Invalid command!")
        except Exception as e:
            print(e)


def list_all_questions():
    questions = question_manager.get_all_questions()
    print_separator()
    print_questions(questions)


def list_all_topics():
    topics = question_manager.get_all_topics()
    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)


def list_random():
    topics = question_manager.get_all_topics()
    if len(topics) == 0:
        print("No topics available! Please create one using 'createTopic'")
        return

    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)

    question_topic_position = int(input("Select question topic: "))
    topic = topics[question_topic_position - 1]

    print_questions(question_manager.get_random_questions(2, topic))


def create_topic():
    name = input("Please enter topic name: ")
    question_manager.create_topic(name)


def create_question():
    topics = question_manager.get_all_topics()
    if len(topics) == 0:
        print("No topics available! Please create one using 'createTopic'")
        return

    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)

    question_topic_position = int(input("Select question topic: "))
    topic = topics[question_topic_position - 1]

    description = input("Enter question description: ")

    answers = [{}, {}, {}, {}]

    print("Please enter 4 answers:")
    for i in range(0, 4):
        answer_description = input("Answer " + str(i + 1) + ": ")
        answers[i][qaf.ANSWER_DESCRIPTION_KEY] = answer_description

    correct_answer_index = int(input("Select the correct answer(Enter a value between 1 and 4): "))
    answers[correct_answer_index - 1][qaf.ANSWER_IS_CORRECT_KEY] = True

    question = question_manager.create_question(description, topic, answers)

    print("Question created successfully!")
    print("--------------")
    print(question)


def delete_question():
    questions = question_manager.get_all_questions()
    print_questions(questions)
    position = int(input("Enter the position of the question from the list above: "))
    affected_records = question_manager.delete_question(questions[position - 1])
    print("Affected records: " + str(affected_records))


def example_save_quiz_run_to_statistics():
    topics = question_manager.get_all_topics()
    if len(topics) == 0:
        print("No topics available! Please create one using 'createTopic'")
        return

    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)

    question_topic_position = int(input("Select question topic: "))

    topic = topics[question_topic_position - 1]
    student_school_name = "School " + uuid.uuid4().hex
    student_year_group = str(random.randint(10, 14)) + "-" + str(random.randint(17, 20))
    questions_and_answers = dict.fromkeys(question_manager.get_random_questions(2, topic), None)

    for question in questions_and_answers:
        picked_answer = random.choice(question.answers)
        questions_and_answers[question] = picked_answer

    quiz_run = statistics_manager.save_quiz_run(topic, student_school_name, student_year_group, questions_and_answers)

    print("Recorded Quiz run:")
    print("School: " + quiz_run.student_school)
    print("Year group: " + quiz_run.student_year_group)
    print("Topic: " + quiz_run.topic.name)

    print("Questions and answers")
    for question_and_answer in quiz_run.questions_and_answers:
        print("Question: " + question_and_answer.question.description)
        print("\tGiven answer: " + str(question_and_answer.selected_answer.description))


def show_help():
    print("questions - display all questions")
    print("topics - display all topics")
    print("createTopic - create a topic")
    print("createQuestion - create a question")
    print("delete - delete a question")
    print("exit - exit the program")


def login_guard():
    if not config_manager.is_admin_logged_in:
        raise Exception("You must be logged in to perform this action!")


def print_questions(questions):
    for index, question in enumerate(questions):
        print("Position: " + str(index + 1))
        print(question)
        print_separator()


def print_separator():
    print("--------------------------------------------------------")
