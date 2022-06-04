import asyncio

def uvloop():
    try:
        import uvloop
    except ImportError:
        return

def start_polling(dp, loop=None):
    uvloop()
    if loop == None:
        loop = asyncio.get_event_loop()

    asyncio.set_event_loop(loop)
    loop.create_task(dp.start_polling())
    loop.run_forever()

