# Server script for Traffic Signal LED Matrix Weather Display

Fetches current weather conditions from [forecast.io](http://forecast.io/),
strips out everything the ESP8266 doesn't need, and puts the result somewhere
under a web server's document root.

# Configuration

First, create a directory under your web server's document root for the weather
data files to be written to.  Whatever user will be running the script must
have write permissions for this directory.

Next, copy config_example.ini to config.ini.  Enter your forecast.io API key
(you _have_ [registered as a developer](https://developer.forecast.io) there
already, right?), latitude, and longitude in config.ini as indicated.  Also
enter the absolute path to the directory you created in the previous paragraph
as `filedest` in the `paths` section.

Set the path to the configuration file as `config_filename` in update.py.  

Set the absolute pathname of the update.py script as `ExecStart` in the
`Service` secton of traffic-display-weather.service.

# Installation

Copy traffic-display-weather.service and traffic-display-weather.timer to
/home/YOURUSERNAME/.config/systemd/user/ .  Enable and start the timer:

    $ systemctl --user enable traffic-display-weather.timer
    $ systemctl --user start traffic-display-weather.service

If you want the timer to start whenever the system boots (rather than when you
log in), you can enable linger:

    # loginctl enable-linger YOURUSERNAME
