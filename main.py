import urequests
import ssd1306
import utime
import json
import network
from machine import I2C, Pin, RTC

rtc = RTC()
i2c = I2C(scl=Pin(4), sda=Pin(5))
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)
wlan = network.WLAN(network.STA_IF)

route = 7
stop = 44
url = 'http://www.m3tma-shuttles.com/Services/JSONPRelay.svc/GetRouteStopArrivals'

error_msg = 'Error'
none_msg = 'None'
shuttle_msg = 'Next Shuttles:'

# each line is 8 pixels high
def next_bus():
    y = 0
    lcd.fill(0)
    print(shuttle_msg)
    lcd.text(shuttle_msg, 0, y)
    y +=16

    try:
        res = urequests.get("{}?RouteID={}&RouteStopID={}".format(url, route, stop))
        if res.status_code != 200:
            res.close()
            return

        js = json.loads(res.text)[0]
        res.close()

        for scheduled in js.get('ScheduledTimes'):
            arrival_str = scheduled.get('ArrivalTimeUTC')
            time = utime.localtime(int(arrival_str[6:16]))
            minutes = (time[3] * 60 + time[4]) - (rtc.now()[3] * 60 + rtc.now()[4])
            msg = "{}:{} in {} min".format(time[3], time[4], minutes)
            print(msg)
            lcd.text(msg, 0, y)
            y += 16
        try:
            scheduled
        except NameError:
            print(none_msg)
            lcd.text(none_msg, 8, y)
            y += 16

    except:
        print(error_msg)
        lcd.text(error_msg, 8, y)
        y += 16

    lcd.text("IP: {}".format(wlan.ifconfig()[0]), 0, y)
    lcd.show()

if __name__ == '__main__':
    while True:
        next_bus()
        utime.sleep(60)
