import asyncio

def uvloop():
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        return

def start_polling(dp, loop=None):
    uvloop()
    if loop == None:
        loop = asyncio.get_event_loop()

    try:
        loop.create_task(dp.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        print('Ctrl+C')
    finally:
        tasks = asyncio.all_tasks(loop=loop)
        for t in tasks:
            t.cancel()
        group = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()
        print('Killed')
