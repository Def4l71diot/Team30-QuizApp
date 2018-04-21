import quiz_app_framework as qaf

from peewee import SqliteDatabase
import getpass

database = SqliteDatabase("quiz_app.db")

qaf.setup(database)

question_manager = qaf.QuestionManager()

config_manager = qaf.ConfigManager()


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
    print_questions([question])


def delete_question():
    questions = question_manager.get_all_questions()
    print_questions(questions)
    position = int(input("Enter the position of the question from the list above: "))
    affected_records = question_manager.delete_question(questions[position - 1])
    print("Affected records: " + str(affected_records))


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
        print("--------")
        print("ID in database: " + str(question.id))
        print("Description: " + question.description)
        print("Image: " + str(question.path_to_image))
        print("Topic: " + question.topic.name)
        print("Answers:")
        for i, answer in enumerate(question.answers):
            print("\t" + str(i + 1) + ". " + answer.description + (" - correct answer" if answer.is_correct else ""))
            print("\t\tImage: " + str(answer.path_to_image))
        print_separator()


def print_separator():
    print("--------------------------------------------------------")
