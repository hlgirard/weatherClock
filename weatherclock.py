# Network imports
try:
    import urequests as requests
except ImportError:
    import requests

try: 
    import ujson as json
except ImportError:
    import json

# Credentials imports
import credentials

# System imports
import os
import time
from micropython import const


BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
INTERVAL = const(10 * 60) # 10 minutes = 600 seconds
SAVE_FILE = 'data/weatherdata.json'

def get_weather_live():
    print('Getting live weather data')
    parameters = {
        'zip': credentials.zip_home + ',' + credentials.country_code,
        'APPID': credentials.owm_API_KEY
    }
    response = requests.get(BASE_URL, params = parameters)

    if response.status_code == 200:
        jWeatherData = response.json()
        jWeatherData['call_dt'] = int(time.time())
        response.close()
        return jWeatherData
    else:
        response.close()
        raise Exception('API Network Request unsucessful, HTTP code: ' + response.status_code)

def get_weather():
    if os.path.isfile(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            curTime = int(time.time())
            if curTime - data['call_dt'] < INTERVAL:
                print('Weather data returned from disk')
                return data
    
    data = get_weather_live()
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
    
    return data


def print_weather(jWeatherData):
    w = jWeatherData
    print('Here is the current weather in ' + w['name'])
    print('The current temperature is ' + str(w['main']['temp']) + ' K')


def main():
    print_weather(get_weather())
