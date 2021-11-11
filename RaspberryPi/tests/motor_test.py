from gpiozero import Motor
from time import sleep

motor = Motor(forward=23, backward=24)
print("init!")

while True:
    motor.forward()
    sleep(5)
    motor.backward()
    sleep(5)


# class gpiozero.PWMOutputDevice(pin, *, active_high=True, initial_value=0, frequency=100, pin_factory=None)

