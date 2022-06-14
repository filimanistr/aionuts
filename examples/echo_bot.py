from aionuts import Bot, Dispatcher, executor

TOKEN = # str
ID = # int
bot = Bot(TOKEN, id=ID, is_group=True)
dp = Dispatcher(bot)

'''
If youll not specify any filters (args inside decorator)
bot will answer to any messages that he recives
'''

@dp.message_handler()
async def echo(msg):
    '''
    will be called by any message
    '''
    await msg.reply(msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)
