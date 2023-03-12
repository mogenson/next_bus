try:
    import requests
except ImportError:
    import urequests as requests

from time import localtime

url = "https://api-v3.mbta.com/predictions?filter[stop]={}&filter[route]={}"


class ArrivalTime:
    def __init__(self, h, m, delta):
        self.h = h
        self.m = m
        self.delta = delta


def get_arrival_times(route, stop):
    timestruct = localtime()
    now = (timestruct[3] * 3600) + (timestruct[4] * 60) + timestruct[5]
    arrival_times = []
    try:
        res = requests.get(url.format(stop, route))
        if res.status_code != 200:
            res.close()
            return arrival_times

        for data in res.json().get("data"):
            arrival_str = (
                data.get("attributes").get("arrival_time").split("T")[1].split("-")[0]
            )
            (h, m, s) = arrival_str.split(":")
            arrival_time = (int(h) * 3600) + (int(m) * 60) + int(s)
            delta = max(arrival_time - now, 0) // 60
            arrival_times.append(ArrivalTime(h, m, delta))

        res.close()
    except Exception as error:
        print(f"{route}: {error}")

    return arrival_times
