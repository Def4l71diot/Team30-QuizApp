# Quiz App framework documentation

# Models

## Topic
`id` - Type: `int` - the id of the topic in database 

`name` - Type: `string` - the name of the topic

## Answer
`id` - Type: `int` the id of the answer in database

`description` - Type: `string` - answer's description

`path_to_image` - Type: `string` - string pointing to the location of the answer's image description - `None` by default

`is_correct` - Type: `bool` - indicates wheter the answer is correct - `False` bu default




## Question
`id` - Type: `int` - the id of the question in database

`description` - Type: `string` - question's description

`path_to_image` - Type: `string` - string pointing to the location of the question's image description - `None` by default

`topic` - Type: `Topic` - question's topic

`answers` - Type: `list<Answer>` - the possible answers for the question


# Managers

## QuestionManager
```python
import quiz_app_framework as qaf

question_manager = qaf.QuestionManager()
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



## ConfigManager
```python
import quiz_app_framework as qaf

config_manager = qaf.ConfigManager()
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
