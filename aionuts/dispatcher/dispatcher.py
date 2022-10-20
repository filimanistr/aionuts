# -*- config: utf-8 -*-

import asyncio
from .handler import Handler
from ..utils.utils import *
from ..types import Message


class Dispatcher:
    """Responsible for sending out something to where it is needed"""
    def __init__(self, bot):
        self.vkbot = bot
        self.message_handlers = Handler()

    async def start_polling(self):
        """Recieves events from the generator
        and creates tasks to process them"""
        request = self.vkbot.lp_loop_gen()
        async for event in request:
            asyncio.create_task(self.process_event(event))

    async def process_event(self, event):
        """Process updates received from long-polling"""
        if self.vkbot.is_group == True:
            if event.type == 'message_new':
                message = Message(self.vkbot, D(event))
                await self.message_handlers.notify(message)

    def message_handler(self, *obj_filters, **kwargs):
        def decorator(callback):
            self.message_handlers.register(callback, obj_filters, kwargs)
            return callback
        return decorator

    def register_message_handler(self, func, *obj_filters, **kwargs):
        self.message_handlers.register(func, obj_filters, kwargs)
