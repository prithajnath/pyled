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
            duty_cycle = value/2.55
            self.pwm.ChangeDutyCycle(duty_cycle/bias)

    def __del__(self):
        self.stop_modulation()

    __repr__ = __str__

