#!/usr/bin/env micropython

import urequests
import ssd1306
from machine import I2C, Pin, RTC

rtc = RTC()
i2c = I2C(scl=Pin(4), sda=Pin(5))
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)

def wifi_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('codewithroot', 'scansorial')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def set_time():
    rtc.ntp_sync(server='pool.ntp.org', update_period=3600, tz='EST5EDT')

route = ['83', '87']
url = ['https://api-v3.mbta.com/predictions?filter[stop]=2299&filter[route]=83&filter[direction_id]=1',
        'https://api-v3.mbta.com/predictions?filter[stop]=2583&filter[route]=87&filter[direction_id]=1']

def next_bus():
    now = (rtc.now()[3] * 3600) + (rtc.now()[4] * 60) + rtc.now()[5]
    lcd.fill(0)
    for i in range(2):
        res = urequests.get(url[i])
        if res.status_code != 200:
            return

        arrival_str = res.json().get('data')[0].get('attributes').get('arrival_time').split('T')[1].split('-')[0]
        (h, m, s) = arrival_str.split(':')
        arrival_time = (int(h) * 3600) + (int(m) * 60) + int(s)
        delta_time = (arrival_time - now) // 60
        y = i * 32
        lcd.text('Next {} bus:'.format(route[i]), 0, y)
        lcd.text(arrival_str, 16, y + 8)
        lcd.text('in {} min'.format(delta_time), 16, y + 16)
        print('Next', route[i], 'bus:', arrival_str, 'in', delta_time, 'min')
        res.close()
    lcd.show()

def do_next_bus():
    import time
    wifi_connect()
    set_time()
    while True:
        next_bus()
        time.sleep(60)
