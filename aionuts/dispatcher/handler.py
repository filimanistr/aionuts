from dataclasses import dataclass
from typing import Callable

from ..utils.utils import *
from .filters import *

class Handler:
    def __init__(self, middleware):
        self.handlers = []
        self.middleware = middleware
        self.filters = {'commands': Command,
                        'chat_type': ChatType}

    def _process_filters(self, obj_filters, kwargs):
        """Iterates over given filters and saves object of each filter
        into a list. Returns that list of objects"""
        filters = list()
        case = kwargs.get('ignore_case', False)
        for key, value in kwargs.items():
            if key in self.filters:
                filters.append(self.filters[key](value))
            else:
                if key != 'ignore_case':
                    filters.append(Default(key, value, ignore_case=case))

        if not not obj_filters:
            filters += [*obj_filters]
        return filters

    def register(self, handler, obj_filters, kwargs):
        """Saves function object and list of it's filters into HandlerObj,
        and passes HandlerObj to a list of all handlers"""
        filters = self._process_filters(obj_filters, kwargs)
        record = Handler.HandlerObj(handler=handler, filters=filters)
        self.handlers.append(record)

    async def check_filters(self, update, filters):
        for f in filters:
            if f.check(update) == False:
                return False
        return True

    async def notify(self, event):
        """Compares filters of the fuction with the recieved message
        and if they match - calls that function"""
        for handler in self.handlers:
            if await self.check_filters(event, handler.filters):
                try:
                    await self.middleware.process_inner_middlewares(event)
                    await handler.handler(event)
                    return None
                except CancelHandler:
                    return None

    @dataclass
    class HandlerObj:
        handler: Callable
        filters: list[object]


class CancelHandler(Exception):
    pass
