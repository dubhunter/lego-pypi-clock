from lib.clock import Clock

clock = Clock(tick_seconds=False, debug=False)

while True:
    clock.loop()
