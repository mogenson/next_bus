import network
import machine
import sys

sys.path[1] = '/flash/lib'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect('ssid', 'password')
    while not wlan.isconnected():
        pass

rtc = machine.RTC()
if not rtc.synced():
    rtc.ntp_sync(server='pool.ntp.org', tz='EST5EDT', update_period=3600)
    while not rtc.synced():
        pass

network.ftp.start(user='micro', password='python', buffsize=1024, timeout=300)
network.telnet.start(user='micro', password='python', timeout=300)
print('IP addr:', wlan.ifconfig()[0])
