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
try:
    import ntptime as time
    DELTA_T =  946684800 # 2000/1/1 - 1970/1/1 Difference between NTP and Unix time.
except ImportError:
    import time
    DELTA_T = 0

BASE_URL = 'http://api.openweathermap.org/data/2.5/'
INTERVAL = 29 * 60 # 29 minutes = 1740 seconds
SAVE_FILE = 'weatherdata.json'
SAVE_FORECAST = 'forecastdata.json'
UNITS = 'metric' # imperial or metric
NUM_LINES = 3 #Limit number of lines in forecast results

def get_weather_live():
    print('Getting live weather data')
    url = BASE_URL + 'weather?APPID={}&id={}&units={}'.format(credentials.owm_API_KEY,credentials.city_id, UNITS)
    response = requests.get(url)

    if response.status_code == 200:
        jWeatherData = response.json()
        jWeatherData['call_dt'] = int(time.time()) + DELTA_T
        response.close()
        return jWeatherData
    else:
        response.close()
        raise Exception('API Network Request unsucessful, HTTP code: ' + response.status_code)

def get_forecast_live():
    print('Getting weather forecast')
    url = BASE_URL + 'forecast?APPID={}&id={}&units={}&cnt={}'.format(credentials.owm_API_KEY, credentials.city_id, UNITS, NUM_LINES)
    response = requests.get(url)

    if response.status_code == 200:
        jForecastData = response.json()
        jForecastData['call_dt'] = int(time.time()) + DELTA_T
        response.close()
        return jForecastData
    else:
        response.close()
        raise Exception('API Network Request unsucessful, HTTP code: ' + response.status_code)

def get_weather():
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            curTime = int(time.time()) + DELTA_T
            if curTime - data['call_dt'] < INTERVAL:
                print('Weather data returned from disk')
            else:
                data = get_weather_live()
                json.dump(data, f)
            return data
    except OSError:
        print('OSError logged in get_weather')
        with open(SAVE_FILE, 'w') as f:
            data = get_weather_live()
            json.dump(data, f)
            return data

def get_forecast():
    try:
        with open(SAVE_FORECAST, 'r') as f:
            data = json.load(f)
            curTime = int(time.time()) + DELTA_T
            if curTime - data['call_dt'] < INTERVAL:
                print('Forecast data returned from disk')
            else:
                data = get_forecast_live()
                json.dump(data, f)
            return data
    except OSError:
        print('OSError logged in get_forecast')
        with open(SAVE_FORECAST, 'w') as f:
            data = get_forecast_live()
            json.dump(data, f)
            return data