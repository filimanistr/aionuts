from aionuts import Bot, Dispatcher, executor

TOKEN = # sample stirng
ID = # sample int
bot = Bot(TOKEN, id=ID, is_group=True)
dp = Dispatcher(bot)

@dp.message_handler()
async def base(msg):
    # msg.event will return a longpull 
    # that came by any SENT message
    await msg.answer(msg.event)


if __name__ == '__main__':
    executor.start_polling(dp)
