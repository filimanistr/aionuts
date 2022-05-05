from dataclasses import dataclass
import asyncio

from . import types

class Prefix():
    # Prefix - a word, letter, or number places before another
    # Default prefix is /
    pass

class Command():
    pass

class Handler:
    def __init__(self):
        self.handlers = []

    def register(self, handler, kwargs):
        record = Handler.HandlerObj(handler=handler, filters=kwargs)
        self.handlers.append(record)

    '''will be fixed, its temporary solutiion'''

    def listify(x):
        """ Try hard to convert x into a list """
        if x != list:
            return [x]
        else:
            return [_ for _ in x]

    async def check_filter(self, text, prefix):
        if len(prefix) == 1:
            if text[0] != prefix:
                return False
        else:
            text = text.split(' ')
            if text[0] != prefix:
                return False

        return True

    async def check_filter_2(self, text, com, prefix):
        text = text.split(' ')
        if len(prefix) == 1:
            if len(text[0]) == 1:
                return False
            if text[0][1:] != com:
                return False

        else:
            if len(text) == 1:
                return False
            if text[1] != com:
                return False

        return True


    async def check_filters(self, update, filters):
        if 'prefixes' in filters.keys():
            if type(filters['prefixes']) == list:
                for prefix in filters['prefixes']:
                    if await self.check_filter(update.text, prefix) == False:
                        return False
                    else:
                        break
            else:
                prefix = filters['prefixes']
                if await self.check_filter(update.text, filters['prefixes']) == False:
                    return False
        else:
            prefix = '/'

        update.prefix = prefix
        for key, value in filters.items():
            if key == 'commands':
                update.command = True
                if type(value) == list:
                    for com in value:
                        if await self.check_filter_2(update.text, com, prefix) == False:
                            return False
                else:
                    if await self.check_filter_2(update.text, value, prefix) == False:
                        return False

            udict = update.__dict__
            if key in udict.keys():
                if udict[key] != value:
                    return False

        return True

    async def notify(self, event):
        # update = event.__dict__
        update = event
        for handler in self.handlers:
            if await self.check_filters(update, handler.filters):
                await handler.handler(event)


    @dataclass
    class HandlerObj:
        handler: callable
        filters: dict
