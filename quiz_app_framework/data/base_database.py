from abc import ABC, abstractmethod
from typing import Type

from peewee import Model


class BaseDatabase(ABC):

    @abstractmethod
    def __init__(self, dao_class: Type[Model]):
        self.dao_class = dao_class

    def get_all(self):
        return self.dao_class.select()

    def get_by_id(self, record_id):
        return self.dao_class.get_by_id(record_id)

    @abstractmethod
    def save(self, object_to_save):
        pass

    # return the number of rows affected
    def update(self, record):
        return record.save()

    def delete(self, record):
        return record.delete_instance()
