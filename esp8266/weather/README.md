# Traffic Signal LED Matrix Weather Display

Displays the current weather conditions.

## Configuration

Set up the server-side script first, found in server/weather.  Then set your
network's SSID and password in weather.py.  Also, set the correct URL of the
trimmed version of the [forecast.io](http://forecast.io/) API call result
(it should be the URL of whatever path you configured for the server-side
script, followed by '/trim.json') in the same file.

## Installation

Copy all the .png and .py files from this directory to the ESP8266.  Install
trafficdisplay.py from esp8266/common to the ESP8266 as well, along with its
dependencies.  Also, install urequests from
[micropython-lib](https://github.com/micropython/micropython-lib) to the
ESP8266.

Reboot the microcontroller, and in a few seconds it should display an icon
depicting the current weather conditions, checking the server for new
information every minute.
