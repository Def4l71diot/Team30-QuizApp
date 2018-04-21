from abc import ABC, abstractmethod

from peewee import fn


class BaseDatabase(ABC):

    @abstractmethod
    def __init__(self, dao_class):
        self.dao_class = dao_class

    def get_all(self):
        return self.dao_class.select()

    def get_by_id(self, record_id):
        return self.dao_class.get_by_id(record_id)

    def get_random(self, number_of_records):
        return self.dao_class.select().order_by(fn.Random()).limit(number_of_records)

    def add(self, **kwargs):
        return self.dao_class.create(**kwargs)

    # return the number of rows affected
    def update(self, record):
        return record.save()

    def delete(self, record):
        return record.delete_instance()
