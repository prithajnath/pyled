import math
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class Channel():

    _channels = {}

    def __new__(cls, name, gpio):

        if gpio in cls._channels:
            return cls._channels[gpio]
        else:
            new_channel = super().__new__(cls)
            new_channel.name = name
            new_channel.gpio = gpio
            cls._channels[gpio] = new_channel

            GPIO.setup(new_channel.gpio, GPIO.OUT)

            new_channel.pwm = GPIO.PWM(new_channel.gpio, 1000)
            new_channel.on = None

            return new_channel

    def gamma(self, nsteps, gamma):
        gammaedUp = [math.pow(x, gamma) for x in range(nsteps)]
        return [x/max(gammaedUp) for x in gammaedUp]

    def rounder(self, topValue, gammas):
        return [min(topValue, round(x*topValue)) for x in gammas]

    def __str__(self):
        return f"{self.name} : {self.gpio}"

    def start_modulation(self):
        if not self.on:
            self.pwm.start(0)
            self.on = True

    def stop_modulation(self):
        if self.on:
            self.pwm.stop()
            self.on = False

    def apply_color(self, value, bias=1):
        if self.on:
            for step in self.rounder(value, self.gamma(16, 2.3)):
                self.pwm.ChangeDutyCycle(step/2.55)
                time.sleep(0.34)

    def __del__(self):
        self.stop_modulation()

    __repr__ = __str__

class LEDStrip():
    def __init__(self, red_pin_number, green_pin_number, blue_pin_number):
        self.red = Channel("red", red_pin_number)
        self.green = Channel("green", green_pin_number)
        self.blue = Channel("blue", blue_pin_number)

        self.palette = []

    def activate(self):
        self.red.start_modulation()
        self.green.start_modulation()
        self.blue.start_modulation()

    def apply_colors(self, r_value, g_value, b_value):
        self.red.apply_color(r_value)
        self.green.apply_color(g_value, bias=1.5)
        self.blue.apply_color(b_value, bias=1.3)

    def add_color(self, r_value, g_value, b_value):
        rgb = (r_value, g_value, b_value)
        if rgb not in self.palette:
            self.palette.append(rgb)

    def apply_random(self):
        rgb = choice(self.palette)
        self.apply_colors(*rgb)


