import socket
import sys
import RPi.GPIO as GPIO
from time import sleep

RUDDER_PIN = 17
SAIL_PIN = 18
CHANGING_VALUE_OF_ANGLE = 20

MOVE = {
    "RUDDER_UP": 1,
    "RUDDER_DOWN": 2,
    "SAIL_UP": 3,
    "SAIL_DOWN": 4,
    "END": 5
}

CLIENT_IP = '0.0.0.0'
CLIENT_PORT = 5555
CLIENT_ADDRESS = (CLIENT_IP, CLIENT_PORT)


class Servo:
    def __init__(self, pin):
        self.pin = pin
        self.frequency = 50
        self.min_angle = 11
        self.max_angle = 169
        self.reset_position = 0
        self.current_angle = 90

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = self.init_pwm()

    def __del__(self):
        self.pwm.stop()

    def init_pwm(self):
        pwm = GPIO.PWM(self.pin, self.frequency)
        pwm.start(self.get_duty_cycle(self.current_angle))
        sleep(0.5)
        pwm.ChangeDutyCycle(self.reset_position)
        return pwm

    def set_angle(self, angle):
        self.current_angle = angle
        duty = self.get_duty_cycle(self.current_angle)

        self.pwm.ChangeDutyCycle(duty)

        sleep(0.1)

        self.pwm.ChangeDutyCycle(self.reset_position)

    def change_angle(self, value):
        if (value < 0 and (self.current_angle > self.min_angle)) or (
                value > 0 and (self.current_angle < self.max_angle)):
            self.current_angle += value
            self.set_angle(self.current_angle)

    @staticmethod
    def get_duty_cycle(angle):
        return angle / 18 + 2.5


class Servo360:
    def __init__(self, pin):
        self.pin = pin
        self.frequency = 50
        self.right_duty = (0.8 / 20) * 100
        self.left_duty = (2.2 / 20) * 100
        self.reset_duty = 0                         # (1.4 / 20) * 100   # uncomment this for RS0616MD servo
        self.current_rotation = 0
        self.bound_rotations = 10

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(self.reset_duty)

    def __del__(self):
        self.pwm.stop()

    def rotate(self, value):
        if self.is_positive(value):
            self.current_rotation += 1
            self.pwm.ChangeDutyCycle(self.right_duty)

        else:
            self.current_rotation -= 1
            self.pwm.ChangeDutyCycle(self.left_duty)

        sleep(0.8)

        self.pwm.ChangeDutyCycle(self.reset_duty)

    def change_angle(self, value):
        if (self.is_positive(value) and (self.current_rotation < self.bound_rotations)) or (
                (not self.is_positive(value)) and (self.current_rotation > 0)):
            self.rotate(value)

    @staticmethod
    def is_positive(value):
        return value >= 0


class Server:
    def __init__(self):
        self.rudder = Servo(RUDDER_PIN)
        self.sail = Servo360(SAIL_PIN)
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(CLIENT_ADDRESS)

    def __del__(self):
        self.socket.close()

    def listen(self):
        while True:
            messages = self.socket.recvfrom(1)
            message = int.from_bytes(messages[0], byteorder='little')
            self.get_move_from_message(message)

    def get_move_from_message(self, message):
        if message == MOVE["RUDDER_UP"]:
            self.rudder.change_angle(CHANGING_VALUE_OF_ANGLE)
        elif message == MOVE["RUDDER_DOWN"]:
            self.rudder.change_angle(-CHANGING_VALUE_OF_ANGLE)
        elif message == MOVE["SAIL_UP"]:
            self.sail.change_angle(CHANGING_VALUE_OF_ANGLE)
        elif message == MOVE["SAIL_DOWN"]:
            self.sail.change_angle(-CHANGING_VALUE_OF_ANGLE)
        elif message == MOVE["END"]:
            sys.exit(0)


def main():
    server = Server()
    try:
        server.listen()
    except KeyboardInterrupt:
        GPIO.cleanup()
        server.socket.close()


if __name__ == '__main__':
    main()
