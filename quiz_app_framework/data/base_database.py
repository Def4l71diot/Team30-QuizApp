from abc import ABC, abstractmethod

from peewee import fn, MySQLDatabase


class BaseDatabase(ABC):

    @abstractmethod
    def __init__(self, dao_class):
        self.dao_class = dao_class

        if isinstance(self.dao_class._meta.database.obj, MySQLDatabase):
            self._db_random_func = fn.Rand
        else:
            self._db_random_func = fn.Random

    def get_all(self):
        return self.dao_class.select()

    def get_by_id(self, record_id):
        return self.dao_class.get_by_id(record_id)

    def get_random(self, number_of_records):
        return self.dao_class.select().order_by(self._db_random_func()).limit(number_of_records)

    def add(self, **kwargs):
        return self.dao_class.create(**kwargs)

    # return the number of rows affected
    def update(self, record):
        return record.save()

    def delete(self, record):
        return record.delete_instance()

    def get_number_of_records(self):
        return self.dao_class.select().count()
