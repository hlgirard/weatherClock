# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()

# Import credentials
from credentials import wifi_password, wifi_ssid

def do_connect():
    '''
    Connect the ESP8266 to the internet
    '''
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    print('Disabling access point interface')
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)


gc.collect()
do_connect()
