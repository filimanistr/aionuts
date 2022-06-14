from aionuts import Bot, Dispatcher, executor

TOKEN = # str
ID = # int
bot = Bot(TOKEN, id=ID, is_group=True)
dp = Dispatcher(bot)

'''
inside decorator you can specify arguments/values
that is returns from vk longpoll response:

test = ''
user_id =
peer_id =
reply_message_text = ''
and other
'''

@dp.message_handler(text='any text.')
async def echo(msg):
    await msg.reply(msg.text)

@dp.message_handler(peer_id=1)
async def byspecialuser(msg):
    await msg.reply('hello pavel')

if __name__ == '__main__':
    executor.start_polling(dp)
