from peewee import Proxy, Model

DATABASE_PROXY = Proxy()


class BaseDAO(Model):
    class Meta:
        database = DATABASE_PROXY
