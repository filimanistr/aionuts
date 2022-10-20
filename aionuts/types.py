import random

class Message:
    """Object that represents a message, that Bot going to send,
    or the message that is already was sent"""
    def __init__(self, vkbot, event):
        """Initialize the variables for a work with the messages"""
        self.vkbot = vkbot
        self.event = event
        self.type = event.type
        self.group_id = event.group_id

        self.prefix = ""
        self.command = None
        if event.type == 'message_new':
            self.id = event.object.message.id
            self.text = event.object.message.text
            self.peer_id = event.object.message.peer_id
            self.from_id = event.object.message.from_id
            self.user_id = event.object.message.from_id
            self.conversation_message_id = event.object.message.conversation_message_id
            if hasattr(event.object.message, 'reply_message'):
                self.reply_message = event.object.message.reply_message
                self.reply_message_text = event.object.message.reply_message.text
                self.reply_message_from_id = event.object.message.reply_message.from_id
                self.reply_message_conversation_message_id = event.object.message.reply_message.conversation_message_id

    def __getattr__(self, atr):
        pass

    @property
    def random_id(self):
        return random.randint(0,2**10)

    def is_command(self):
        if self.command is None:
            return False
        return True

    def get_args(self):
        """If message is a command, then this method will return message
        without a command and a prefix inside the text. Example:
        if message is `/help me pls`, then the return would be: `me pls`"""
        if self.is_command() == False:
            return self.text

        if len(self.prefix) == 1:
            text = self.text.split(' ', 1)
            if len(text) > 1:
                return text[1]

        text = self.text.split(' ', 2)
        if len(text) > 2:
            return text[2]
        return ""

    def get_command(self):
        """If message is command and starts with: `/help` or `bot help`
        the return string would be: `help`"""
        if self.is_command() == False:
            return None
        try:
            if len(self.prefix) == 1:
                return self.text.split(' ', 1)[0][1:]
            else:
                return self.text.split(' ', 2)[1]
        except IndexError:
            return ''

    def get_prefix(self):
        """If message is command and starts with: `/help` or `bot help`
        then the return string would be: `/` or `bot`"""
        if len(self.prefix) == 1:
            return self.text.split(' ')[0][0]
        else:
            return self.text.split(' ')[0]

    async def answer(self, message, **kwargs):
        """Send a message to a user, that sent a message"""
        await self.vkbot.call('messages.send',
                              peer_id=self.peer_id,
                              random_id=self.random_id,
                              message=message,
                              d=kwargs)

    async def reply(self, message, **kwargs):
        """Reply to a message, that had come to a bot"""
        await self.vkbot.call('messages.send',
                              peer_id=self.peer_id,
                              random_id=self.random_id,
                              reply_to=self.id,
                              message=message,
                              d=kwargs)

    async def edit(self, message, **kwargs):
        await self.vkbot.call('messages.edit',
                conversation_message_id=self.conversation_message_id,
                peer_id=self.peer_id,
                message=message,
                d=kwargs)

    async def delete(self):
        await self.vkbot.messages.delete(
                conversation_message_ids=self.conversation_message_id,
                delete_for_all=1,
                peer_id=self.peer_id,
                group_id=self.group_id)

