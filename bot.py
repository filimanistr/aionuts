# -*- config: utf-8 -*-

import asyncio
import json, random
from functools import partial

from .vkapi import vk
from .vkapi.utils import *

from .handler import Handler
from .types import Message, Callback, Update

def uvloop():
    try:
        import uvloop
    except ImportError:
        return

def start_polling(bot, loop=None):
    uvloop()
    if loop == None:
        loop = asyncio.get_event_loop()

    asyncio.set_event_loop(loop)
    loop.create_task(bot.vkbot.lp_loop(longpoll, bot))
    loop.run_forever()

async def longpoll(event, bot):
    print(event)
    asyncio.create_task(bot.process_event(event))

class Bot:
    def __init__(self, TOKEN, ID):
        self.vkbot = vk.vk(TOKEN, id=ID, is_group=True)
        self.message_handlers = Handler()
        self.callback_handlers = Handler()

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
