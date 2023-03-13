from mbta import MBTA

try:
    import asyncio
except ImportError:
    import uasyncio as asyncio

try:
    from micropython import const
except ImportError:
    const = lambda x: x

TEELE_SQ = const(2576)
DAVIS_SQ = const(70063)
UPDATE_PERIOD = const(15)


def log(route, secs, fresh):
    pass
    now = time.time()
    tm = time.localtime(secs)
    delta = max((secs - now) // 60, 0)
    print(f"{route}: {tm[3]}:{tm[4]} in {delta} min {'*' if fresh else ' '}")


async def do_87_bus():
    route = "87 Bus"
    bus_87 = MBTA(route.split()[0], TEELE_SQ)
    while True:
        times, fresh = bus_87.get_arrival_times()
        if len(times):
            log(route, times[0], fresh)
        await asyncio.sleep(UPDATE_PERIOD)


async def do_88_bus():
    route = "88 Bus"
    bus_88 = MBTA(route.split()[0], TEELE_SQ)
    while True:
        times, fresh = bus_88.get_arrival_times()
        if len(times):
            log(route, times[0], fresh)
        await asyncio.sleep(UPDATE_PERIOD)


async def do_red_line():
    route = "Red Line"
    red_line = MBTA(route.split()[0], DAVIS_SQ)
    while True:
        times, fresh = red_line.get_arrival_times()
        if len(times) >= 2:
            log(route, times[0], fresh)
            log(route, times[1], fresh)
        await asyncio.sleep(UPDATE_PERIOD)


async def main():
    tasks = (
        asyncio.create_task(do_87_bus()),
        asyncio.create_task(do_88_bus()),
        asyncio.create_task(do_red_line()),
    )
    try:
        await asyncio.gather(*tasks)
    except Exception as error:
        print(error)
        import machine

        machine.soft_reset()


if __name__ == "__main__":
    asyncio.run(main())
