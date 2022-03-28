# -*- config: utf-8 -*-

import asyncio, uvloop
import json, random
from urllib.request import urlopen
from functools import partial

from .vkapi import vk
from .vkapi.utils import *

from .handler import Handler
from .types import Message, Callback, Update


def start_polling(bot):
    uvloop.install()
    loop = asyncio.get_event_loop()

    try:
        queue = asyncio.LifoQueue() # Тут собираются апдейты от вк
        loop.create_task(bot.vkbot.lp_loop(longpoll, queue))
        loop.create_task(bot.start_polling(queue))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        # loop.stop()
        pass

'''
def start_polling(bot):
    uvloop.install()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(bot.vkbot.lp_loop(longpoll, bot))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        # loop.stop()
        pass
'''

async def longpoll(event, queue):
    print(event)
    await queue.put(event)
    # asyncio.create_task(bot.process_event(event))


class Bot:
    def __init__(self, TOKEN, ID):
        self.vkbot = vk.vk(TOKEN, id=ID, is_group=True)
        self.message_handlers = Handler()
        self.callback_handlers = Handler()

    async def start_polling(self, queue):
        self._polling = True

        while self._polling:
            event = await queue.get()
            asyncio.create_task(self.process_event(event))

    async def process_event(self, event):
        '''Process updates received from long-polling'''
        '''Сжечь все н, и написать заново'''
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
