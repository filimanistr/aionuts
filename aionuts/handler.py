from dataclasses import dataclass
import asyncio

from . import types

class Handler:
    def __init__(self):
        self.handlers = []

    def register(self, handler, kwargs):
        record = Handler.HandlerObj(handler=handler, filters=kwargs)
        self.handlers.append(record)

    async def check_filters(self):
        pass

    async def notify(self, event):
        update = event.__dict__
        for handler in self.handlers:
            for key, value in handler.filters.items():
                if key in update.keys():
                    if update[key] == value:
                        await handler.handler(event)

    @dataclass
    class HandlerObj:
        handler: callable
        filters: dict
