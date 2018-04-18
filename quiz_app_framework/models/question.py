class Question:

    def __init__(self, description, topic, answers, correct_answer, path_to_image=None):
        self.id = None
        self.description = description
        self.topic = topic
        self.answers = answers
        self.correct_answer = correct_answer
        self.path_to_image = path_to_image

