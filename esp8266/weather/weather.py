import network
import time
import ujson

import urequests

import trafficdisplay

ssid = 'Belkin_G_Plus_MIMO_AA65F1'
password = ''
forecast_proxy = 'http://192.168.0.34/.weather/trim.json'

known_icons = ('clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind',
    'fog', 'cloudy', 'partly-cloudy-day', 'partly-cloudy-night')

def main():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass

    td = trafficdisplay.TrafficDisplay(speed=0)
    old_icon_filename = ''

    while True:
        req = urequests.get(forecast_proxy)
        weather_info = ujson.loads(req.text)
        icon = weather_info['currently']['icon']
        icon_filename = '{}.png'.format(icon) if icon in known_icons else 'matrix.png'
        if icon_filename != old_icon_filename:
            td.load_png(icon_filename)
        old_icon_filename = icon_filename
        td.start(2)
        time.sleep(60)
