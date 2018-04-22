import quiz_app_framework as qaf

from peewee import SqliteDatabase
database = SqliteDatabase("quiz_app.db")

qaf.setup(database)

question_manager = qaf.QuestionManager()

def run():
	start_command = input("Type 'start' to start the quiz: ")
	while start_command != "start":
		print("Invalid command.")
		start_command = input("Type 'start' to start the quiz: ")
	print("Okay, lets start the quiz.")
	print()

	questions = question_manager.get_random_questions(2)
	print(questions)



run()