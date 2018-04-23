# Quiz App framework documentation

# Setup 
```python
import quiz_app_framework as qaf

database = SqliteDatabase("quiz_app.db")

# supports all databases supported by peewee
framework = qaf.Framework(database)
```

# Models

## Topic
`id` - Type: `int` - the id of the topic in database 

`name` - Type: `string` - the name of the topic

## Answer
`id` - Type: `int` - the id of the answer in database

`description` - Type: `string` - answer's description

`path_to_image` - Type: `string` - string pointing to the location of the answer's image description - `None` by default

`is_correct` - Type: `bool` - indicates wheter the answer is correct - `False` bu default


## Question
`id` - Type: `int` - the id of the question in database

`description` - Type: `string` - question's description

`path_to_image` - Type: `string` - string pointing to the location of the question's image description - `None` by default

`topic` - Type: `Topic` - question's topic

`answers` - Type: `list<Answer>` - the possible answers for the question

`is_deleted` - Type: `bool` - indicates whether the question has been deleted

`number_of_times_answered_correctly` - Type: `int` 

`number_of_times_answered_incorrectly` - Type: `int`

`number_of_times_skipped` - Type: `int`

`number_of_times_asked` - Type: `int` - the total number of times the question was asked

`percentage_answered_correctly` - Type: `float` - percentage of time the question is answered correctly

`percentage_answered_incorrectly` - Type: `float` - percentage of time the question is answered incorrectly

`percentage_skipped` - Type: `float` - percentage of time the question is skipped

## AnsweredQuestion
`question` - Type: `Question` - the question

`selected_answer` - Type: `Answer` - the answer that was given to the question - `None` if the question was not answered(skipped)

## QuizRun
`student_year_group` - Type: `string` - the year group of the student who took the quiz

`student_school` - Type: `string`  - the school of the student who took the quiz

`topic` - Type: `topic` - the topic of the quiz

`questions_and_answers` - Type: `list<AnsweredQuestion>` - all questions asked in the quiz and the answers give to them - see `AnsweredQuestion`

# Managers

## QuestionManager
```python
question_manager = framework.question_manager
```
### Methods
#### `create_topic(topic_name)` -> `Topic`
Creates new topic and adds it to database

returns the newly created `Topic`

#### `get_all_topics()` -> `list<Topic>`
Retrieves all topics from database

#### `get_topic(topic_id)` -> `Topic`
Retrieves topic with id `topic_id` from database

#### `create_question(description, topic, answers, path_to_image=None)` -> `Question`
Creates a new question and adds it to database

`description` - Type: `string` - question's description

`topic` - Type: `Topic` - question's topic

`answers` - Type: `list<dict>` - questions's answers - **See example**

`path_to_image` - Type: `string` - path that points to the question's image - **optional**

returns the newly created `Question`

Example:
```python
description = "The description of the question"
topic = question_manager.get_topic(1)
path_to_image = "C:\\Users\\apicture.png"

answer = {
    qaf.ANSWER_DESCRIPTION_KEY: "Answer 1"
}

answer_with_image = {
    qaf.ANSWER_DESCRIPTION_KEY: "Answer with picture",
    qaf.ANSWER_PATH_TO_IMAGE_KEY: "C:\\Users\\pictureforanswer.png"
}

second_answer[qaf.ANSWER_IS_CORRECT_KEY] = True

answers = [answer, answer_with_image]

question = qaf.create_question(description, topic, answers)

question_with_image = qaf.create_question(description, topic, answers, path_to_image=path_to_image)
```

#### `update_question(question)` -> `int`
Updates an existing question

`question` - Type: `Question` - the modified version of the question

returns the number of rows affected in database

Example:
```python
question = question_manager.get_question(1)

question.description = "new description"

question_manager.update_question(question)
```

#### `delete_question(question)` -> `int`
Deletes an existing question

`question` - Type: `Question` - the question to delete

returns the number of rows in database affected

Example:
```python
question = question_manager.get_question(1)

question_manager.delete_question(question)
```

#### `get_all_questions()` -> `list<Question>`
Retrieves all questions from database

#### `get_question(question_id)` -> `Question`
Retrieves question with id `topic_id` from database

#### `get_random_questions(number_of_questions, topic=None)` -> `list<Question>`
Retrieves `number_of_questions` random questions

Retrieves `number_of_questions` random questions with `topic`

`topic` - Type: `Topic` - the random questions retrieved must be with this topic - **optional**

Example:
```python
ten_random_questions = question_manager.get_random_questions(10)

topic = question_manager.get_topic(1)

five_random_questions_with_topic = question_manager.get_random_questions(5, topic)
```

## StatisticsManager
```python
statistics_manager = framework.statistics_manager
```

### Methods

#### `mark_question_answered_correctly(question)` -> `void`
Marks a question as correctly answered

`question` - the question to mark as correctly answered

#### `mark_question_answered_incorrectly(question)` -> `void`
Marks a question as incorrectly answered

`question` - the question to mark as incorrectly answered

#### `mark_question_skipped(question)` -> `void`
Marks a question as skipped

`question` - the question to mark as skipped

#### `mark_question_was_asked(question)` -> `void`
Marks a question as asked

`question` - Type: `Question` - the question to mark as asked

#### `get_hardest_question()` -> `Question` or `None`
Retrieves the question with the highest `percentage_answered_incorrectly`

returns the hardest question
if none of the questions was asked, returns `None` 

#### `save_quiz_run(topic, student_school, student_year_group, questions_and_answers)` -> `QuizRun`
Saves a quiz run

`topic` - Type: `Topic` - the topic of the quiz

`student_school` - Type: `string`  - the school of the student who took the quiz

`student_year_group` - Type: `string` - the year group of the student who took the quiz

`questions_and_answers` - Type: `dict<Question, Answer>` - dictionary whose keys are the questions asked in the quiz

returns the newly created entry in database

Example:
```python
student_school = "School 1"
student_year_group = "16-19"

topic = question_manager.get_topic(1)

questions = question_manager.get_random_questions(3, topic=topic)

questions_and_answers = dict.fromkeys(questions, None)

    for question in questions_and_answers:
        picked_answer = random.choice(question.answers)
        questions_and_answers[question] = picked_answer


quiz_run = statistics_manager.save_quiz_run(topic, student_school, student_year_group, questions_and_answers)

```

#### `get_all_quiz_runs()` -> `list<QuizRun>`
Retrieves all quiz runs


## ConfigManager
```python
config_manager = framework.config_manager
```

### Properties
`is_first_launch` - indicates wheter it's the first time the app is launched - returns `bool`

`is_admin_logged_in` - indicates wheter the admin user is logged in - returns `bool`

### Methods
#### `login_admin(password)` -> `bool`
Validates admin login 

returns `True` if the password is correct, `False` if not

#### `register_admin(password)` -> `bool`
Registers the admin user

returns `True` if the admin user was created successfuly, `False` if not

#### `logout_admin()` -> `void`
Logouts the admin
