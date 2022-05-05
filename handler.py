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

    def listify(self, x):
        """ Try hard to convert x into a list """
        if type(x) != list:
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
        for key, value in filters.items():
            filters[key] = self.listify(value)

        if 'ignore_case' in filters.keys():
            '''Ignore case for prefixes and commands'''
            if filters['ignore_case'] == [True]:
                update.text = update.text.lower()
                for key, value in filters.items():
                    for v in value:
                        if type(v) == str:
                            filters[key] == v.lower()

        if 'prefixes' in filters.keys():
            for prefix in filters['prefixes']:
                state = await self.check_filter(update.text, prefix)
                if state == True:
                    break

            if state == False:
                return False

        else:
            prefix = '/'

        update.prefix = prefix
        for key, value in filters.items():
            if key == 'commands':
                update.command = True
                for com in value:
                    state = await self.check_filter_2(update.text, com, prefix)
                    if state == True:
                        break

                if state == False:
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
