class Answer:

    def __init__(self, description, is_correct=False, path_to_image=None):
        self.id = None
        self.description = description
        self.is_correct = is_correct
        self.path_to_image = path_to_image
