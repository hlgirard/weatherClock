import datarepo

def print_weather(jWeatherData):
    w = jWeatherData
    print('Here is the current weather in ' + w['name'])
    print('The current temperature is ' + str(w['main']['temp']) + ' K')


def main():
    #print_weather(datarepo.get_weather()) #Test weather data retrieval
