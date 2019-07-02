import network
import machine
import sys
import display

sys.path[1] = '/flash/lib'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect('ssid', 'password')
    while not wlan.isconnected():
        pass

print('IP addr:', wlan.ifconfig()[0])
tft = display.TFT()
tft.init(tft.ILI9341, width=240, height=320, miso=19, clk=18, mosi=23,
         dc=21, cs=5, backl_pin=14, backl_on=1, rot=tft.LANDSCAPE_FLIP)
tft.text(0,0, wlan.ifconfig()[0])

rtc = machine.RTC()
if not rtc.synced():
    rtc.ntp_sync(server='pool.ntp.org', tz='EST5EDT', update_period=3600)
    while not rtc.synced():
        pass

network.ftp.start(user='micro', password='python', buffsize=1024, timeout=300)
network.telnet.start(user='micro', password='python', timeout=300)
print('IP addr:', wlan.ifconfig()[0])
