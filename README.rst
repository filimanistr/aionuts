Aionuts 

Основная идея проекта - использование декораторов в python, за место if else логики, избавление от громостких блоков чем то более подходящим, а так же ускорение работы за счет использования асинхронности.

Синтаксис и большинство команд приемствуются с другого подобного фреймворка - aiogram. Это сделано с расчетом на возможность изменения лишь нескольких строчек, для перенисения/переписания бота от апи телеграмма на апи Вконтакте.

Установка:

pip install aionuts

Простой пример использования:

from aionuts import Bot, Dispatcher, executor

bot = Bot(YOUR_TOKEN, id=YOUR_ID, is_group=True)
dp = Dispatcher(bot)

@dp.message_handler()
async def base(msg):
    if (msg.event['object']['message']['text'] == 'hi')
        await msg.answer('hello')

executor.start_polling(dp)
