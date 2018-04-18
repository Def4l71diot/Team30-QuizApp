from .models.base_model import DATABASE_PROXY


def setup(database):
    DATABASE_PROXY.initialize(database)
