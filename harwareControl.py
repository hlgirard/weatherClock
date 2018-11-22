# Servo duty cycle from 30 to 115 leads to 180 degree rotation.
from machine import PWM, Pin
from math import floor
from time import sleep

class Servo:

    def __init__(self, pin, angle = 90, freq = 50):
        self.freq = freq
        self.pin = pin
        self.pwm = PWM(Pin(pin), freq=freq, duty=77)
        self.goto(angle)

    def goto(self, angle):
        duty_cycle = floor(30 + angle/180 * (115-30))
        print('Going to angle {} with duty cycle {}'.format(angle, duty_cycle))
        self.pwm.duty(duty_cycle)
        print(self.pwm.duty())
        sleep(1)
        self.pwm.deinit()

servo = Servo(14)