from dataclasses import dataclass
import asyncio

from . import types

class Prefix():
    '''Prefix - a word, letter, or number places before another'''
    def check(self, message, prefix, ignore_case):
        message.prefix = prefix # value in filter
        text = message.get_prefix() # value from vk message
        if ignore_case:
            prefix = prefix.lower()
            text = text.lower()

        if text == prefix:
            return True
        return False

class Command():
    def check(self, message, command, ignore_case):
        message.command = True
        text = message.get_command()
        if ignore_case:
            command = command.lower() # value in filter
            text = text.lower() # value from vk message

        if text == command:
            return True
        return False

class Default():
    '''compare filters with vk longpoll
    peer_id, text, from_id and other stuff'''
    def check(self, update, key, value, ignore_case):
        update = update.__dict__
        if ignore_case:
            value = value.lower()

        if key in update.keys():
            if update[key] == value:
                return True
        return False

class Handler:
    def __init__(self):
        self.handlers = []
        self.filters = {'prefixes': Prefix(),
                        'commands': Command()}

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

    async def check_filter(self, update, filters, ignore_case, cls):
        for value in filters:
            if cls.check(update, value, ignore_case):
                return True
        return False

    async def check_defaults(self, update, filters):
        cls = Default()
        for key in filters.keys():
            if key not in self.filters.keys() and key != 'ignore_case':
                for value in filters[key]:
                    if cls.check(update, key, value, filters['ignore_case'][0]):
                        break
                    else:
                        return False
        return True

    async def check_filters(self, update, filters):
        for key, value in self.filters.items():
            if key in filters.keys():
                args = (update, filters[key], filters['ignore_case'][0], value)
                passed = await self.check_filter(*args)
                if passed == False:
                    return False

        if await self.check_defaults(update, filters) == False:
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
