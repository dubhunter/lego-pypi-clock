import math
import time
from buildhat import Motor, Hat
from datetime import datetime

TOTAL_DEGREES = 360
HOURS_PER_REV = 12
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
HOUR_DEGREES_PER_MINUTE = TOTAL_DEGREES / HOURS_PER_REV / MINUTES_PER_HOUR
MINUTE_DEGREES_PER_SECOND = TOTAL_DEGREES / MINUTES_PER_HOUR / SECONDS_PER_MINUTE

HOUR_PORT = 'A'
MINUTE_PORT = 'B'


class Clock:
    def __init__(self, tick_seconds, debug):
        self.debug = debug
        self.tick_seconds = tick_seconds

        self.hat = Hat()

        self.hour_hand = Motor(HOUR_PORT)
        self.minute_hand = Motor(MINUTE_PORT)

        self.hour_hand.release = False
        self.minute_hand.release = False

    @staticmethod
    def degrees_to_motor_angle(degrees: int):
        return 360 - degrees if degrees > 180 else 0 - degrees

    def log(self, msg):
        if self.debug:
            print(msg)

    def move_hand(self, hand: Motor, degrees: int):
        self.log(f"Degrees: {degrees}")
        angle = self.degrees_to_motor_angle(degrees)
        self.log(f"Angle: {angle}")
        hand.run_to_position(angle, blocking=False, direction='shortest')

    def loop(self):
        self.hat.set_leds(color='both')

        now = datetime.now()

        self.log(f"{now.hour}:{now.minute}:{now.second}")

        hour_percent = now.hour % HOURS_PER_REV / HOURS_PER_REV
        minute_percent = now.minute / MINUTES_PER_HOUR

        hour_degrees = math.floor(TOTAL_DEGREES * hour_percent) + math.floor(now.minute * HOUR_DEGREES_PER_MINUTE)
        minute_degrees = math.floor(TOTAL_DEGREES * minute_percent)
        if self.tick_seconds:
            minute_degrees +=  math.floor(now.second * MINUTE_DEGREES_PER_SECOND)

        self.log("Hour hand...")
        self.move_hand(self.hour_hand, hour_degrees)

        self.log("Minute hand...")
        self.move_hand(self.minute_hand, minute_degrees)

        self.log("Sleeping...")

        time.sleep(0.5)

        self.hat.set_leds(color='green')

        time.sleep(0.5)
