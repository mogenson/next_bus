from machine import I2C, Pin
from writer import Writer
import freesans20
import schedule
import ssd1306
import time

# display
lcd = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(4), sda=Pin(5)))
writer = Writer(lcd, freesans20)
lcd.fill(0)
lcd.text("IP: {}".format(wlan.ifconfig()[0]), 0, 56)
lcd.show()


def print_time():
    h, m = time.localtime()[3:5]
    s = "{}:{:02}".format(h, m)
    print(s)

    writer.set_textpos(20, 40)
    writer.printstring(s)
    lcd.show()


# tasks
print_time()
schedule.every().minute.do(print_time)

# main loop
while True:
    schedule.run_pending()
    time.sleep(1)
