#!/usr/bin/env python3
# update.py - Dirty Python script to grab the parts of a forecast.io API
# response that the traffic display wants

import configparser
import json
import requests

# Load the configuration file
config_filename = '/home/clay/traffic-display-weather/config.ini'
config = configparser.ConfigParser()
config.read(config_filename)

# Make the forecast.io API call
url = 'https://api.forecast.io/forecast/{}/{},{}'.format(
        config['forecast']['key'],
        config['forecast']['lat'],
        config['forecast']['lon'])
req_result = requests.get(url)

# Save the API call result to the web server
with open('{}/full.json'.format(config['paths']['filedest']), 'w') as full:
    full.write(req_result.text)

# Cut out the part we want and save that
data = json.loads(req_result.text)

trimmed_data = {
    'currently': {
        'icon': data['currently']['icon']
    }
}

with open('{}/trim.json'.format(config['paths']['filedest']), 'w') as trim:
    trim.write(json.dumps(trimmed_data))
