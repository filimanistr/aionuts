from aionuts import Bot, Dispatcher, executor

TOKEN = # str
ID = # int
bot = Bot(TOKEN, id=ID, is_group=True)
dp = Dispatcher(bot)

'''
by default commands starts with /
you can change this by specifying prefixes
'''

@dp.message_handler(commands='inc', prefixes='!')
async def inc(msg):
    '''
    will be called when user sends '!inc'

    you can get message's text, without command and prefix by calling
    msg.get_args()
    '''
    num = msg.get_args()
    num = int(num) + 1
    await msg.reply(num)

@dp.message_handler(commands=['decrement', 'dec'], prefixes=['anyword', 'w'])
async def dec(msg):
    '''
    will be called when user sends 'anyword dec' or 'w dec' or ...

    to get message's prefix call
    msg.get_prefix()

    to get command
    msg.get_command
    '''

    await msg.reply(msg.get_args())
    await msg.reply(msg.get_command())
    await msg.reply(msg.get_prefix())

if __name__ == '__main__':
    executor.start_polling(dp)
