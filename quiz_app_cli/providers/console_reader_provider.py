from pyinputedittext import input_edit_text
from getpass import getpass


class ConsoleReaderProvider:

    def read_input(self, prompt="", value_for_editing="", strip=True):
        if not value_for_editing:
            console_input = input(prompt)
        else:
            console_input =  input_edit_text(prompt, text_to_edit=value_for_editing)

        return console_input.strip() if strip else console_input

    def read_input_hidden(self, prompt=""):
        return getpass(prompt)
