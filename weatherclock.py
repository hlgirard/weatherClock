# Imports
from time import sleep

# Module imports
import datarepo
import hardwareControl

# Constants
CAT_SERVO_PIN = 14
MIN_TEMP = -25
MAX_TEMP = 50
LOOP_DELAY = 30 * 60 # 30 minutes = 1800 seconds

#Weather conditions
NUM_CONDITIONS = 7
BLACK_ICE = 0
FREEZING = 1
SNOWING = 2
RAINING = 3
COOL = 4
PERFECT = 5
HOT = 6

def weatherType(jWeatherData, jForecastData):

    w = jWeatherData
    f = jForecastData

    temp = w['main']['temp']
    rainForecast = False
    snowForecast = False

    # Determing whether rain or snow is forecast in the next 6 to 9 hours
    for i in range(3):
        c = f['list'][i]['weather'][0]['id']
        if c // 100 == 5 or c // 100 == 2: # Weather condition is rain or thunderstorm
            rainForecast = True
        elif c // 100 == 6: # Weather condition is snow
            snowForecast = True

    if 'rain' in w and temp < 0:
        print('Black ice possible')
        return BLACK_ICE
    elif 'snow' in w or snowForecast:
        print("Snowing")
        return SNOWING
    elif 'rain' in w or rainForecast:
        print('Raining')
        return RAINING
    elif temp < 5:
        print("It's freezing outside!")
        return FREEZING
    elif temp < 15:
        print("It's cold outside")
        return COOL
    elif temp > 28:
        print("It's too hot")
        return HOT
    else:
        print('The weather is perfect today!')
        return PERFECT
        

def main():

    #Initialize
    catServo = hardwareControl.CategoryServo(CAT_SERVO_PIN, NUM_CONDITIONS)

    #History Variables
    prevCond = -1

    #Main Loop
    while True:
        w = datarepo.get_weather()
        f = datarepo.get_forecast()

        condition = weatherType(w, f)

        if condition != prevCond:
            catServo.setCategory(condition)
            prevCond = condition
        
        sleep(LOOP_DELAY)

if __name__ == '__main__':
        main()