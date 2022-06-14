from aionuts import Bot, Dispatcher, executor

TOKEN = # str
ID = # int
bot = Bot(TOKEN, id=ID, is_group=True)
dp = Dispatcher(bot)

'''
When message is recieved, bot will check all the decorators
untill he finds one that fits the filters (args inside decorator)
'''

@dp.message_handler(commands=['hello', 'h'])
async def hello(msg):
    '''
    will be called when user sends /hello or /h
    '''
    await msg.answer("Hello")

@dp.message_handler(commands='help')
async def hello(msg):
    '''
    alternatively, you can call vk methods by referring to the bot class:
    bot.users.get(user_id = 1)
    bot.account.ban(...)

    see https://dev.vk.com/method
    '''
    await bot.messages.send(peer_id = msg.peer_id,
                            random_id = msg.random_id,
                            message = "help")

if __name__ == '__main__':
    executor.start_polling(dp)
