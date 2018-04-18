from peewee import Proxy, Model

DATABASE_PROXY = Proxy()


class BaseModel(Model):
    class Meta:
        database = DATABASE_PROXY
