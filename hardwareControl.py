# Servo duty cycle from 30 to 115 leads to 180 degree rotation.
from machine import PWM, Pin
from math import floor
from time import sleep

class Servo:
    """
    Provides methods to actuate a servomotor

    Parameters
    ----------
    pin : int
        GPIO pin number of the signal line of the servo
    angle : int, optional 0 < angle < 180
        Initialization angle of the servo, default 90
    freq : int, optional
        Frequency of the PWM signal to control the servo, default 50 Hz

    Methods
    -------
    goto(angle)
        Moves the servo to the specified angle and removes power from it
    """

    def __init__(self, pin, angle = 90, freq = 50):
        self.freq = freq
        self.pin = pin
        self.pwm = PWM(Pin(pin), freq=freq, duty=77)
        self.goto(angle)

    def goto(self, angle):
        if angle < 0 or angle > 180:
            raise ValueError('Servo: angle is outside permissible range ({})'.format(angle))
        duty_cycle = floor(30 + angle/180 * (115-30))
        self.pwm.duty(duty_cycle)
        sleep(1)
        self.pwm.deinit()

class TempServo(Servo):
    """
    Provides methods to actuate a servomotor to display temperature in a half circle scale

    Parameters
    ----------
    pin : int
        GPIO pin number of the signal line of the servo
    minTemp : int
        Temperature corresponding to 0º angle
    maxTemp : int
        Temperature corresponding to 180º angle

    Methods
    -------
    setTemp(temp)
        Moves the servo to the angle corresponding to the specified temperature and removes power from it
    """

    def __init__(self, pin, minTemp, maxTemp):
        Servo.__init__(self, pin)
        self.minTemp = minTemp
        self.maxTemp = maxTemp

    def setTemp(self, temp):
        if temp < self.maxTemp and temp > self.minTemp:
            angle = floor((temp - self.minTemp)/(self.maxTemp - self.minTemp) * 180)
            self.goto(angle)
        else:
            raise ValueError('Temperature is outside permissible range')

class CategoryServo(Servo):

    def __init__(self, pin, numCategories):
        Servo.__init__(self, pin)
        self.numCat = numCategories

    def setCategory(self, category):
        if category < 0 or category > self.numCat:
            raise ValueError('Category outside allowable range')
        else:
            angle = category / self.numCat * 180
            self.goto(angle)