from gpiozero import PWMOutputDevice
from time import sleep

# class gpiozero.PWMOutputDevice(pin, *, active_high=True, initial_value=0, frequency=100, pin_factory=None)

motor = PWMOutputDevice(23)
print("init!")

while True:
	print("is_active", motor.is_active)
	print("frequency", motor.frequency)
	print("value", motor.value)
	motor.pulse(fade_in_time=1, fade_out_time=1, n=None, background=True)
	sleep(3)
	motor.blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True)
	sleep(3)
	motor.toggle()
	sleep(3)
	motor.on()
	sleep(3)
	motor.off()
	sleep(3)


# class gpiozero.PWMOutputDevice(pin, *, active_high=True, initial_value=0, frequency=100, pin_factory=None)
# is_active
# value
# frequency
# pulse(fade_in_time=1, fade_out_time=1, n=None, background=True)
# toggle()
# on()
# off()
# blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True)

