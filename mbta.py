try:
    import urequests as requests
except ImportError:
    import requests

try:
    from micropython import const
except ImportError:
    const = lambda x: x

import time
import re

URL = const("https://api-v3.mbta.com/predictions?filter[stop]={}&filter[route]={}")
ISO8601 = re.compile("^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)")


class MBTA:
    def __init__(self, route: str, stop: str | int):
        self.route = route
        self.stop = stop
        self.arrival_times: list[int] = []
        self.update_time: int = int(time.time())

    def get_arrival_times(self) -> list[int]:  # list of seconds since midnight
        now = int(time.time())
        if now < self.update_time:
            return self.arrival_times, False  # cached results

        self.arrival_times = []
        try:
            res = requests.get(URL.format(self.stop, self.route))
            if res.status_code != 200:
                res.close()
                return self.arrival_times

            tm = time.localtime()
            for data in res.json().get("data"):
                arrival_str = data.get("attributes").get("arrival_time")
                arrival_datetime = tuple(
                    map(int, ISO8601.match(arrival_str).groups())
                ) + (
                    (
                        0,
                        0,
                        tm[8],
                    )
                    if len(tm) == 9
                    else (0, 0)
                )
                arrival_time = int(time.mktime(arrival_datetime))
                self.arrival_times.append(arrival_time)

            res.close()
            if len(self.arrival_times):
                # update again halfway to the first arrive time, or 1 minute in the future
                self.update_time = max((self.arrival_times[0] - now) // 2, now + 60)
        except Exception as error:
            print(error)

        return self.arrival_times, True  # fresh results


if __name__ == "__main__":
    mbta = MBTA("88", 2576)
    times, fresh = mbta.get_arrival_times()
    now = int(time.time())
    for seconds in times:
        timestruct = time.localtime(seconds)
        delta = max((seconds - now) // 60, 0)
        print(f"88 Bus: {timestruct[3]}:{timestruct[4]} in {delta} min")
