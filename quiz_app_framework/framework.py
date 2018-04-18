from peewee import Model


class Framework:
    BASE_MODEL = None

    @staticmethod
    def setup(database_connection):
        class BaseModel(Model):
            class Meta:
                database = database_connection

        Framework.BASE_MODEL = BaseModel
