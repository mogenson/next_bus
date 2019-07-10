from machine import I2C, Pin
from writer import Writer
import freesans20
import ssd1306
import time

# display
lcd = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(4), sda=Pin(5)))
writer = Writer(lcd, freesans20)


def print_ip():
    lcd.fill(0)
    lcd.text("IP: {}".format(wlan.ifconfig()[0]), 0, 56)


def print_time():
    h, m = time.localtime()[3:5]
    s = "{}:{:02}".format(h, m)
    print(s)

    print_ip()
    writer.set_textpos(20, 40)
    writer.printstring(s)
    lcd.show()


def print_traffic():
    s = "traffic"
    print(s)

    print_ip()
    writer.set_textpos(20, 40)
    writer.printstring(s)
    lcd.show()


minute = 0
counter = 0

print_time()

while True:
    time.sleep(1)

    tm = time.localtime()
    if tm[4] == minute:
        continue

    minute = tm[4]

    # do traffic monday-friday between 4:00 and 4:59 PM
    if tm[6] < 5 and tm[3] == 16:
        if counter == 0:
            print_traffic()
            counter = 5  # wait 5 minutes before making a new request
        else:
            counter -= 1
    else:
        print_time()
        counter = 0
