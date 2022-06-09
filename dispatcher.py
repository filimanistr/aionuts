# -*- config: utf-8 -*-

import asyncio
import json, random
from functools import partial

from .utils.utils import *

from .handler import Handler
from .types import Message, Callback, Update


class Dispatcher:
    '''a person who is responsible for sending
    out something to where they are needed'''
    def __init__(self, bot):
        self.vkbot = bot
        self.message_handlers = Handler()
        self.callback_handlers = Handler()

    async def start_polling(self):
        '''Recieves events from the generator
        and creates tasks to process them'''
        request = self.vkbot.lp_loop_gen()
        async for event in request:
            if event is not None:
                print(event)
                asyncio.create_task(self.process_event(event))

    async def process_event(self, event):
        '''Process updates received from long-polling'''
        update = D(event)
        update = Update(self.vkbot, update)
        if update.type == 'message_new':
            message = Message(self.vkbot, event)
            await self.message_handlers.notify(message)
        if event.type == 'message_event':
            callback = Callback(self.vkbot, event)
            await self.callback_handlers.notify(callback)

    def message_handler(self, **kwargs):
        def decorator(callback):
            self.message_handlers.register(callback, kwargs)
            return callback
        return decorator

    def callback_handler(self, **kwargs):
        def decorator(callback):
            self.callback_handlers.register(callback, kwargs)
            return callback
        return decorator

    def register_message_handler(self, func, **kwargs):
        self.message_handlers.register(func, kwargs)
