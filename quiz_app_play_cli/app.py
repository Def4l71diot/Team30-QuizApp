import quiz_app_framework as qaf

from peewee import SqliteDatabase
database = SqliteDatabase("quiz_app.db")

framework = qaf.Framework(database)

question_manager = framework.question_manager
statistics_manager = framework.statistics_manager

def run():
	# school info code
	number_of_questions = 3
	score = []
	start_command = input("Type 'start' to start the quiz: ")
	while start_command != "start":
		print("Invalid command.")
		start_command = input("Type 'start' to start the quiz: ")
	print("Okay, lets start the quiz.")
	print("To restart the quiz at anytime type 'restart'")
	print()
	print("Do you wish to choose a topic?")
	print("0. No Topic")
	topics = question_manager.get_all_topics()
	list_all_topics()
	print()
	
	question_topic_position = input("Please select a topic: ")
	while True:
		try:
			int(question_topic_position)
			break
		except ValueError:
			if question_topic_position == "restart":
				print("restarting quiz")
				print()
				run()
			else:
				print("Invalid input")
				question_topic_position = input("Type 'no' or select a topic: ")
	
	while (int(question_topic_position) < 0) or (int(question_topic_position) > len(topics)) :
		print("Invalid input")
		question_topic_position = input("Type 'no' or select a topic: ")

	if int(question_topic_position) == 0:
		questions = question_manager.get_random_questions(number_of_questions)
	else:
		topic = topics[int(question_topic_position) - 1]
		questions = question_manager.get_random_questions(number_of_questions, topic=topic)

	print()

 	schools = []
 	while True:
 		schools.append(input("Enter attending school: "))
 		command = get_schools()
 		if command == "n":
 			break
 
 	start(questions, number_of_questions, schools, score)
	

def get_schools():
	valid_input = False
	while valid_input == False:
		command = input("Add another school(y/n): ")
		if command == "y":
			valid_input = True
		elif command == "n":
			return command
		else:
			print("Invalid Input")

def start(questions, number_of_questions, schools, score):
	while True:
		print()
		Schools_string = ", ".join(schools)
		print("Schools: " + Schools_string)
		valid_input = False
		while valid_input == False:
			school = input("Enter School: ")
			if school in schools:
				valid_input = True
			else:
				print("Invalid Input")

		i = 0
		while i < number_of_questions:
			print()
			correct = quiz(questions, i)
			if correct == False:
				score.append(0)
			else:
				score.append(1)
			i = i + 1
		displayScore(score, number_of_questions)

def quiz(questions, i):
		skip = False
		quiz = displayQuestion(questions[i])
		correct_answer = quiz[0]
		correct_answer_description = quiz[1]
		chosen_answer = input("Please choose an answer, or type 'skip': ")
		
		if chosen_answer == "restart":
			print("restarting quiz")
			print()
			run()
		if chosen_answer == "skip":
			print("skipping question")
			print()
			statistics_manager.mark_question_skipped(questions[i])
			skip = True
			correct = False
		if skip == False:
			while True:
				try: 
					int(chosen_answer)
					break
				except ValueError:
						if chosen_answer == "skip":
							print("skipping question")
							print()
							correct = False
							statistics_manager.mark_question_skipped(questions[i])
							skip = True
							break
						else:
							print("Invalid input. Please ensure you input a number.")
							chosen_answer = input("Please choose an answer: ")
		while skip == False:
			while (int(chosen_answer) > 4 or int(chosen_answer) < 1):
				print("Invalid choice")
				chosen_answer = input("Please choose an answer: ")
			if int(chosen_answer) == correct_answer:
				print()
				print("--Correct--")
				print()
				correct = True
				statistics_manager.mark_question_answered_correctly(questions[i])
			else:
				print()
				print("--Incorrect--")
				print("Correct answer was " + correct_answer_description)
				print()
				correct = False
				statistics_manager.mark_question_answered_incorrectly(questions[i])
			skip = True

		return(correct)
		


def list_all_topics():
	topics = question_manager.get_all_topics()
	for index, topic in enumerate(topics):
	    print(str(index + 1) + ". " + topic.name)


def displayQuestion(questions):
	print("Question: " + questions.description)
	statistics_manager.mark_question_was_asked(questions)
	for i, answer in enumerate(questions.answers):
		if answer.is_correct:
		    correct_answer = i + 1
		    correct_answer_description = answer.description
		print( "Answer "+ str(i + 1) + ". " + answer.description)
		print( "Image: " + str(answer.path_to_image))
	

	return([correct_answer,correct_answer_description])

def displayScore(score, number_of_questions):
	total_score = sum(score)
	print("You scored " + str(total_score) + " out of " + str(number_of_questions))
	print("Percentage: " + str(round((total_score/number_of_questions)*100)) + "%")
