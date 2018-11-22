# Imports
from time import sleep

# Module imports
import datarepo
import hardwareControl

# Constants
TEMP_SERVO_PIN = 14
MIN_TEMP = -25
MAX_TEMP = 50
LOOP_DELAY = 10 #seconds


def print_weather(jWeatherData):
    w = jWeatherData
    print('Here is the current weather in ' + w['name'])
    print('The current temperature is ' + str(w['main']['temp']) + ' K')


def main():

    #Initialize
    servo = hardwareControl.TempServo(TEMP_SERVO_PIN, MIN_TEMP, MAX_TEMP)

    #Main Loop
    while True:
        w = datarepo.get_weather()
        temp_c = w['main']['temp'] - 273.15 #K to C conversion
        print('The current temperature is {} ºC'.format(temp_c))
        servo.setTemp(temp_c)

        sleep(LOOP_DELAY)


