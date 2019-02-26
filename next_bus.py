import urequests
import ssd1306
from machine import I2C, Pin, RTC

rtc = RTC()
i2c = I2C(scl=Pin(4), sda=Pin(5))
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)

stop = ['2299', '2583']
route = ['83', '87']
url = 'https://api-v3.mbta.com/predictions?filter[stop]={}&filter[route]={}&filter[direction_id]=1'


def next_bus():
    now = (rtc.now()[3] * 3600) + (rtc.now()[4] * 60) + rtc.now()[5]
    lcd.fill(0)
    for i in range(2):
        y = i * 32
        try:
            res = urequests.get(url.format(stop[i], route[i]))
            if res.status_code != 200:
                res.close()
                return

            arrival_str = res.json().get('data')[0].get('attributes').get(
                'arrival_time').split('T')[1].split('-')[0]
            (h, m, s) = arrival_str.split(':')
            arrival_time = (int(h) * 3600) + (int(m) * 60) + int(s)
            delta_time = (arrival_time - now) // 60
            lcd.text('Next {} bus:'.format(route[i]), 0, y)
            lcd.text(arrival_str, 16, y + 8)
            lcd.text('in {} min'.format(delta_time), 16, y + 16)
            print('Next', route[i], 'bus:',
                  arrival_str, 'in', delta_time, 'min')
            res.close()
        except:
            lcd.text('Next {} bus: Error'.format(route[i]), 0, y)
            print('Next', route[i], 'bus: Error')
    lcd.show()


def do_next_bus():
    import time
    while True:
        next_bus()
        time.sleep(60)
