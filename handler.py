from dataclasses import dataclass
import asyncio

from . import types

class Command():
    def get_prefix(self, message, filters):
        prefix = message.text.split()[0]
        if filters.get('ignore_case')[0] is True:
            prefix = prefix.lower()

        if filters.get('prefixes') is None:
            return '/' if prefix[0] == '/' else None
        if prefix in filters['prefixes']:
            return prefix
        if prefix[0] in filters['prefixes']:
            return prefix[0]
        return None

    def check(self, message, filters):
        prefix = self.get_prefix(message, filters)
        if prefix is None:
            return False

        message.prefix = prefix
        message.command = True
        command = message.get_command()
        commands = filters['commands']
        if filters.get('ignore_case')[0] is True:
            command = command.lower()

        if command in commands:
            return True
        return False

class ChatType():
    def check(self, message, filters):
        if filters['chat_type'][0] == 'private':
            if message.peer_id < 2000000000:
                return True
        return False

class Default():
    '''compare filters with vk longpoll
    peer_id, text, from_id and other stuff'''
    def check(self, update, filters, f):
        update = update.__dict__
        if filters.get('ignore_case')[0] is True:
            if type(update[f]) is str:
                update[f] = update[f].lower()

        if update[f] in filters[f]:
            return True
        return False

class Handler:
    def __init__(self):
        self.handlers = []
        self.filters = {'commands': Command(),
                        'chat_type': ChatType()}

    def register(self, handler, kwargs):
        for key, value in kwargs.items():
            kwargs[key] = self.listify(value)

        record = Handler.HandlerObj(handler=handler, filters=kwargs)
        self.handlers.append(record)

    def listify(self, x):
        """ Try hard to convert x into a list """
        if type(x) != list:
            return [x]
        else:
            return [_ for _ in x]

    async def check_filters(self, update, filters):
        for f, value in filters.items():
            if f in self.filters.keys():
                cls = self.filters[f]
                if cls.check(update, filters) == False:
                    return False

            elif f in update.__dict__.keys():
                cls = Default()
                if cls.check(update, filters, f) == False:
                    return False

        return True

    async def notify(self, event):
        for handler in self.handlers:
            if await self.check_filters(event, handler.filters):
                await handler.handler(event)

    @dataclass
    class HandlerObj:
        handler: callable
        filters: dict
