import quiz_app_framework as qaf

from peewee import SqliteDatabase

database = SqliteDatabase("quiz_app.db")

qaf.setup(database)

question_db = qaf.QuestionDatabase()
topic_factory = qaf.TopicFactory()
answer_factory = qaf.AnswerFactory()
question_factory = qaf.QuestionFactory()

def run():
    while True:
        try:
            command = input("Please enter a command: ")
            if command == "questions":
                list_all_questions()
            elif command == "topics":
                list_all_topics()
            elif command == "createTopic":
                create_topic()
            elif command == "createQuestion":
                create_question()
            elif command == "delete":
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
    questions = question_db.get_all()
    print_separator()
    print_questions(questions)


def list_all_topics():
    topics = question_db.get_all_topics()
    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)


def create_topic():
    name = input("Please enter topic name: ")
    topic = topic_factory.create_topic(name)
    question_db.save_topic(topic)


def create_question():
    topics = question_db.get_all_topics()
    if len(topics) == 0:
        print("No topics available! Please create one using 'createTopic'")
        return

    for index, topic in enumerate(topics):
        print(str(index + 1) + ". " + topic.name)

    question_topic_position = int(input("Select question topic: "))
    topic = topics[question_topic_position - 1]

    description = input("Enter question description: ")
    answers = [None] * 4
    print("Please enter 4 answers:")

    for i in range(0, 4):
        answer_description = input("Answer " + str(i + 1) + ": ")
        answer = answer_factory.create_answer(answer_description)
        answers[i] = answer

    correct_answer_index = int(input("Select the correct answer(Enter a value between 1 and 4): "))
    answers[correct_answer_index - 1].is_correct = True

    question = question_factory.create_question(description, topic, answers)
    question_from_database = question_db.save(question)

    print("Question created successfully!")
    print("--------------")
    print_questions([question_from_database])


def delete_question():
    questions = question_db.get_all()
    print_questions(questions)
    position = int(input("Enter the position of the question from the list above: "))
    affected_records = question_db.delete(questions[position - 1])
    print("Affected records: " + str(affected_records))


def show_help():
    print("questions - display all questions")
    print("topics - display all topics")
    print("createTopic - create a topic")
    print("createQuestion - create a question")
    print("delete - delete a question by it's position in the 'list' command")
    print("exit - exit the program")


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
