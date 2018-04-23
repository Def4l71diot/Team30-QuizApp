import quiz_app_framework as qaf

from peewee import SqliteDatabase
database = SqliteDatabase("quiz_app.db")

framework = qaf.Framework(database)

question_manager = framework.question_manager
statistics_manager = framework.statistics_manager

def run():
	
	score = []
	print()
	start_command = input("Type 'start' to start the quiz: ")
	while start_command != "start":
		print("Invalid command.")
		start_command = input("Type 'start' to start the quiz: ")
	print("Okay, lets start the quiz.")
	
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
				question_topic_position = input("Pleae select a topic: ")
	
	while (int(question_topic_position) < 0) or (int(question_topic_position) > len(topics)) :
		print("Invalid input")
		question_topic_position = input("Pleae select a topic: ")
	

	if int(question_topic_position) == 0:
		topic = 0
		
	else:
		topic = topics[int(question_topic_position) - 1]

	print()
	number_of_questions = int(input("How many questions to ask each vistor?: "))
	print()

	schools = []
	while True:
		schools.append(input("Please enter attending school: ").lower())
		command = get_schools()
		if command == "n":
			break


	start(number_of_questions, schools, score, topic)

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

def start(number_of_questions, schools, score, topic):
	
	while True:
		print()
		topic = topic

		if topic == 0:
			questions = question_manager.get_random_questions(number_of_questions)
		else:
			questions = question_manager.get_random_questions(number_of_questions, topic=topic)
		print()
		Schools_string = ", ".join(schools)
		print("Schools: " + Schools_string)
		valid_input = False
		while valid_input == False:
			school = input("What school do you attend?: ")
			if school.lower() in schools:
				valid_input = True
			else:
				print("Invalid Input")
		print()
		print("What Year Group are you in? e.g if you are in Year 8 type '8'")
		year_group = input("Year Group: ")

		i = 0
		questions_and_answers = {}
		while i < number_of_questions:
			print()
			correct = quiz(questions, i, number_of_questions, schools, score, topic)
			if correct[0] == False:
				score.append(0)
			else:
				score.append(1)
			questions_and_answers[questions[i]] = correct[1]
			i = i + 1
		displayScore(score, number_of_questions)
		statistics_manager.save_quiz_run(topic= topic, student_school=school, student_year_group=year_group, questions_and_answers=questions_and_answers)

def quiz(questions, i, number_of_questions, schools, score, topic):
		print("To restart the quiz at anytime type 'restart'")
		print()
		skip = False
		skipped = False
		quiz = displayQuestion(questions[i])
		correct_answer = quiz[0]
		correct_answer_description = quiz[1]
		
		chosen_answer = input("Please choose an answer, or type 'skip': ")
		
		if chosen_answer == "restart":
			print("restarting quiz")
			print()
			start(number_of_questions, schools, score, topic)
		if chosen_answer == "skip":
			print("skipping question")
			print()
			statistics_manager.mark_question_skipped(questions[i])
			skip = True
			skipped = True
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
		if skipped == False:
			return(correct, questions[i].answers[int(chosen_answer)-1])
		else: 
			return(correct, 0)
		


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
	