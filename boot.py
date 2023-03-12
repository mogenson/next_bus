import time

import utelnetserver
import network
import ntptime
import machine

# connect to wifi
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect("THE_INTERNET", "seriesoftubes")
while not nic.isconnected():
    time.sleep(1)
print(nic.ifconfig()[0])

# set time and convert to EST (don't worry about date or year)
ntptime.settime()
tm = time.gmtime()
offset = -5 if tm[3] >= 5 else 19
machine.RTC().datetime(
    (tm[0], tm[1], tm[2], tm[6] + 1, tm[3] + offset, tm[4], tm[5], 0)
)

# start telnet server
utelnetserver.start()
