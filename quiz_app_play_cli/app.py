import quiz_app_framework as qaf

from peewee import SqliteDatabase
database = SqliteDatabase("quiz_app.db")

qaf.setup(database)

question_manager = qaf.QuestionManager()

def run():
	number_of_questions = 3
	start_command = input("Type 'start' to start the quiz: ")
	while start_command != "start":
		print("Invalid command.")
		start_command = input("Type 'start' to start the quiz: ")

	print("Okay, lets start the quiz.")
	print("To restart the quiz at anytime type 'restart'")
	print()

	questions = question_manager.get_random_questions(number_of_questions)
	i = 0
	while i < number_of_questions:
		quiz(questions, i)
		i = i + 1


def quiz(questions, i):
		correct_answer = displayQuestion(questions[i])
		chosen_answer = input("Please choose an answer: ")
		if chosen_answer == "restart":
			print("restarting quiz")
			print()
			run()
		else:
			while (int(chosen_answer) > 4 or int(chosen_answer) < 1):
				print("Invalid choice")
				chosen_answer = input("Please choose an answer: ")
			if int(chosen_answer) == correct_answer:
				print("Correct")
				correct = True
			else:
				print("Incorrect")
				correct = False

		return(correct)
		





def displayQuestion(questions):
	print("Question: " + questions.description)
	for i, answer in enumerate(questions.answers):
		if answer.is_correct:
		    correct_answer = i + 1
		print( "Answer "+ str(i + 1) + ". " + answer.description)
		print( "Image: " + str(answer.path_to_image))
	    
	return(correct_answer)

