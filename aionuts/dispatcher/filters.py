from ..utils.utils import *


class Command():
    """Command filter"""
    def __init__(self, commands, prefixes=['/'], ignore_case=False):
        self.commands = listify(commands)
        self.prefixes = listify(prefixes)
        self.ignore_case = ignore_case

    def _get_prefix(self, msg):
        """Checks if message contains any of specified prefixes"""
        prefix = msg.split()[0]
        if prefix in self.prefixes:
            return prefix
        if prefix[0] in self.prefixes:
            return prefix[0]
        return None

    def _get_command(self, msg, p):
        """Checks if message contains any of specified commands"""
        text = msg.split()
        if len(p) == 1:
            return text[0][1:]
        if len(text) > 1:
            return text[1]
        return None

    def check(self, message):
        """If message contains any of the prefix and commands specified in
        the filters, then we suppliment the message class with the new data:
         message.command, message.prefix"""
        if message.text == "":
            return False

        msg = message.text
        if self.ignore_case == True:
            self.commands = [c.lower() for c in self.commands]
            self.prefixes = [p.lower() for p in self.prefixes]
            msg = msg.lower()

        prefix = self._get_prefix(msg)
        if prefix is None:
            return False

        command = self._get_command(msg, prefix)
        if command is None:
            return False

        if command in self.commands:
            message.command = command
            message.prefix = prefix
            return True
        return False


class ChatType():
    def __init__(self, chat_type):
        self.chat_type = chat_type

    def check(self, message):
        if self.chat_type == 'private':
            if message.peer_id < 2000000000:
                return True
        return False


class Default():
    """Compares filters with vk longpoll json's keys
    peer_id, text, from_id and other stuff"""
    def __init__(self, key, value, ignore_case=False):
        self.key = key                  # filter set by the user
        self.value = listify(value)     # value of the filter
        self.ignore_case = ignore_case

    def check(self, update):
        update = update.__dict__
        value = update.get(self.key)
        if value is None:
            print("Unknown filter: ", self.key)
            return False

        if self.ignore_case is True:
            if type(update[self.key]) is str:
                value = value.lower()

        if value in self.value:
            return True
        return False
