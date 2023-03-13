import time

import utelnetserver
import network
import time
import ntptime
import machine

# connect to wifi
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect("THE_INTERNET", "seriesoftubes")
while not nic.isconnected():
    time.sleep(1)
print(nic.ifconfig()[0])

# set time and convert to local timezone
secs = ntptime.time()
dst = True
secs -= (5 - int(dst)) * 3600
tm = time.gmtime(secs)
machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
print(time.localtime())


# start telnet server
utelnetserver.start()
