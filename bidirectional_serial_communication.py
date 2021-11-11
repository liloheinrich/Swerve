#!/usr/bin/env python3
import serial
import time

motor1_speed = 0.75
motor2_speed = -0.82
motor3_speed = 0.3444
motor4_speed = -0.314
servo1_angle = 101
servo2_angle = 82
servo3_angle = 3
servo4_angle = 21

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser2.flush()
    while True:

        # ser.write(b"Hello from Raspberry Pi!\n"
        ser.write(bytes(str(motor1_speed)+","+str(motor2_speed)+","+str(motor3_speed)+"\n"))
        line = ser.readline().decode('utf-8').rstrip()
        print("Arduino 1 says: " + str(line))

        # ser2.write(b"Hello from Raspberry Pi!\n"
        ser2.write(bytes(str(motor4_speed)+","+str(servo1_angle)+","+str(servo2_angle)+","+str(servo3_angle)+","+str(servo4_angle)+"\n"))
        line = ser2.readline().decode('utf-8').rstrip()
        print("Arduino 2 says: " + str(line))

        time.sleep(1)

    
        