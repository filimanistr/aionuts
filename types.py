import asyncio
import random

class Update:
    def __init__(self, vkbot, event):
        self.vkbot = vkbot
        self.type = event.type
        self.group_id = event.group_id

    @property
    def random_id(self):
        return random.randint(0,2**10)


class Message(Update):
    '''Object that represents a message, that Bot going to send, or the message that is already was sent'''
    def __init__(self, vkbot, event):
        '''Initialize the variables for a work with the messages'''
        super().__init__(vkbot, event)

        self.prefix = '/'
        self.command = False
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

    def get_args(self):
        if self.command == False:
            return self.text
        else:
            if len(self.prefix) == 1:
                text = self.text.split(' ', 1)
                if len(text) == 1: return ''
                else: return text[1]
            else:
                text = self.text.split(' ', 2)
                if len(text) == 2: return ''
                else: return text[2]

    def is_command(self):
        return self.command

    def get_command(self):
        if self.command:
            try:
                if len(self.prefix) == 1:
                    return self.text.split(' ', 1)[0][1]
                else:
                    return self.text.split(' ', 2)[1]
            except IndexError:
                return ''

    def get_prefix(self):
        if len(self.prefix) == 1:
            return self.text.split(' ')[0][0]
        else:
            return self.text.split(' ')[0]

    async def answer(self, message, **kwargs):
        '''Send a message to a user'''
        await self.vkbot.call('messages.send',
                              peer_id=self.peer_id,
                              random_id=self.random_id,
                              message=message,
                              d=kwargs)

    async def reply(self, message, **kwargs):
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
        '''Delete a message'''
        await vkbot.messages.delete(
                conversation_message_ids=self.conversation_message_id,
                delete_for_all=1,
                peer_id=self.peer_id,
                group_id=self.group_id)

class Callback(Message):
    def __init__(self, vkbot, event):
        super().__init__(vkbot, event)

        self.is_command = False
        self.type == event.type
        self.user_id = event.object.user_id
        self.peer_id = event.object.peer_id
        self.event_id = event.object.event_id
        self.payload = event.object.payload
        self.conversation_message_id = event.object.conversation_message_id

        self.callback = self.payload['callback']

    def is_command(self):
        return self.is_command

    def _split_callback(self, event, **kwargs):
        callback = {'user_id': self.message.user_id, 'event': event}
        for key, value in kwargs.items(): callback[key] = value
        return json.dumps(callback)

    async def answer(self, message, **kwargs):
        '''Send a message to a user'''
        await self.vkbot.call('messages.send', peer_id=self.peer_id, random_id=self.random_id, message=message, d=kwargs)

    async def edit(self, message, **kwargs):
        '''Doing something'''
        await self.vkbot.call('messages.edit', conversation_message_id=self.conversation_message_id,
                peer_id=self.peer_id, message=message, d=kwargs)


class Keyboard():
    '''Keyboard class that implements the keyboard in easiest way'''
    def __init__(self, inline, keyboard=None):
        '''Defines the new clear keyboard and sets the type of it - inline or not
        If the keyboard attribute was set - convert it into python dict object'''
        if keyboard != None: self.keyboard = json.loads(keyboard)
        else: self.keyboard = {"inline":inline, "buttons":[]}

    def __repr__(self):
        '''Returns the keyboard'''
        return json.dumps(self.keyboard)

    def add_column(self, type_, payload, label, color):
        '''Adds button to the right'''
        if len(self.keyboard['buttons']) == 0: self.keyboard['buttons'].append([])
        self.keyboard['buttons'][0].append({'action':{'type':type_, 'payload':payload, 'label':label}, 'color':color})

    def add_row(self, type_, payload, label, color):
        '''Adds button to the buttom)'''
        self.keyboard["buttons"].append([{"action":{"type":type_, "payload":payload, "label":label}, "color":color}])

class InlineKeyboard:
    '''Клавиатура только калл бэковская изначально (обрезание, ой т.е. инкапсуляция)'''
    def __init__(self):
        self.keyboard = {"inline":True, "buttons":[]}

    def __repr__(self):
        '''Returns the keyboard'''
        return json.dumps(self.keyboard)

    def add_column(self, text, callback, color, callback_data=None):
        '''Adds button to the right'''
        payload = self.callback(callback, callback_data)
        if len(self.keyboard['buttons']) == 0: self.keyboard['buttons'].append([])
        self.keyboard['buttons'][0].append({'action':{'type':'callback', 'payload':payload, 'label':text}, 'color':color})

    def add_row(self, text, callback, color, callback_data=None):
        '''Adds button to the buttom)'''
        payload = self.callback(callback, callback_data)
        self.keyboard["buttons"].append([{"action":{"type":'callback', "payload":payload, "label":text}, "color":color}])

    def callback(self, payload, callback_data):
        '''Делает из 2 каллов 1 калл'''
        callback = dict()
        callback['callback'] = payload
        if callback_data != None:
            for key, value in callback_data.items():
                callback[key] = value

        return callback

'''
class InlineKeyboardButton:
    def __init__(self, text, callback, callback_data=None):
'''
