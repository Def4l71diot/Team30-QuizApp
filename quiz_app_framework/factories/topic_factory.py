from quiz_app_framework.models import Topic


class TopicFactory:

    def create_topic(self, name):
        return Topic(name)
