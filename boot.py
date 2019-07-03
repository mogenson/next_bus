import machine
import network
import sys

# path for import modules
sys.path[1] = '/flash/lib'

# wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect('ssid', 'password')
    while not wlan.isconnected():
        pass
print('IP addr:', wlan.ifconfig()[0])

# time
rtc = machine.RTC()
if not rtc.synced():
    rtc.ntp_sync(server='pool.ntp.org', tz='EST5EDT')
    while not rtc.synced():
        pass

# ftp + telnet: user='micro', password='python'
network.ftp.start()
network.telnet.start()
