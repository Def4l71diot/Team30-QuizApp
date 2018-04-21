from quiz_app_framework.data import BaseDatabase
from quiz_app_framework.models import Topic


class TopicDatabase(BaseDatabase):

    def __init__(self):
        super().__init__(Topic)

    def add(self, **kwargs):
        return self.dao_class.get_or_create(name=kwargs["name"])
