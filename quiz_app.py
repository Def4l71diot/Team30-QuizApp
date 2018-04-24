#!/usr/bin/python3
from quiz_app_cli import App
from quiz_app_cli.providers import *

from quiz_app_framework import Framework
from peewee import SqliteDatabase

DATABASE_FILENAME = "quiz_app.db"


def main():
    database = SqliteDatabase(DATABASE_FILENAME)
    framework = Framework(database)

    reader = ConsoleReaderProvider()
    writer = ConsoleWriterProvider()

    app = App(framework.config_manager,
              framework.question_manager,
              framework.statistics_manager,
              reader,
              writer)

    app.run()


if __name__ == "__main__":
    main()
