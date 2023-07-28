import asyncio


async def wait_temperature_reach_consign(first):
    for i in range(10, 20):
        print(first, i)
        await asyncio.sleep(1)
    pass


async def do_something_else(auther):
    for i in range(0, 15):
        print(auther, i)
        await asyncio.sleep(1)
    pass


async def several_methods_run_together():
    statements = [wait_temperature_reach_consign("a"), do_something_else("b")]
    await asyncio.gather(*statements)
    print("finish")


if __name__ == "__main__":
    # execute only if run as a script
    asyncio.run(several_methods_run_together())
