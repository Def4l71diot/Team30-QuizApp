import os


class ConsoleWriterProvider:
    SEPARATOR = "---------------------------"

    def write(self, text="", end="\n"):
        print(text, end=end)

    def write_separator(self):
        print(self.SEPARATOR)

    # reference:
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python Jan 18 '10 at 7:34
    # Clears the terminal/cmd
    def clear(self):
        os.system("cls||clear")
    # end reference
