import RPi.GPIO as GPIO

class AlphaBot:

    def __init__(self, speed=50):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pin motori
        self.IN1 = 12
        self.IN2 = 13
        self.IN3 = 20
        self.IN4 = 21

        self.EN_A = 6
        self.EN_B = 26

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        GPIO.setup(self.EN_A, GPIO.OUT)
        GPIO.setup(self.EN_B, GPIO.OUT)

        self.pwm_a = GPIO.PWM(self.EN_A, 1000)
        self.pwm_b = GPIO.PWM(self.EN_B, 1000)

        self._speed = max(0, min(100, speed))
        self.pwm_a.start(self._speed)
        self.pwm_b.start(self._speed)

        self.stop()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = max(0, min(100, value))
        self.pwm_a.ChangeDutyCycle(self._speed)
        self.pwm_b.ChangeDutyCycle(self._speed)

    def increase_speed(self, step=10):
        self.speed = self._speed + step

    def decrease_speed(self, step=10):
        self.speed = self._speed - step

    def forward(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def cleanup(self):
        self.stop()
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()
