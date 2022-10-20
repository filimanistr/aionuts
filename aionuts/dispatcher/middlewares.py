

class Middleware:
    def __init__(self):
        # list of objects
        self.middlewares = list()

    def setup(self, middleware):
        self.middlewares.append(middleware)

    async def process_inner_middlewares(self, event):
        for middleware in self.middlewares:
            await middleware.on_process_message(event, None)


class BaseMiddleware:
    async def on_process_message(self, message, _):
        """This handler is called when dispatcher receives a message"""
        return
