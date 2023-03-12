from mbta import get_arrival_times

try:
    import asyncio
except ImportError:
    import uasyncio as asyncio

teele_sq = "2576"
davis_sq = "70063"


def log(route, time):
    print(f"{route}: {time.h}:{time.m} in {time.delta} min")


async def wait(delta):
    await asyncio.sleep(max(delta // 2 * 60, 60))


async def do_87_bus():
    route = "87 Bus"
    time = get_arrival_times(route.split()[0], teele_sq)[0]
    log(route, time)
    while True:
        await wait(time.delta)
        time = get_arrival_times(route.split()[0], teele_sq)[0]
        log(route, time)


async def do_88_bus():
    route = "88 Bus"
    time = get_arrival_times(route.split()[0], teele_sq)[0]
    log(route, time)
    while True:
        await wait(time.delta)
        time = get_arrival_times(route.split()[0], teele_sq)[0]
        log(route, time)


async def do_red_line():
    route = "Red Line"
    times = get_arrival_times(route.split()[0], davis_sq)
    log(route, times[0])
    log(route, times[1])
    while True:
        await wait(times[1].delta)
        times = get_arrival_times(route.split()[0], davis_sq)
        log(route, times[0])
        log(route, times[1])


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
