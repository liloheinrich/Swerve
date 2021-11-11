#!/usr/bin/env python3
import serial
import time

timeout = 0.1 # time to wait before sending next data

test_motor_speeds = [0.1*i for i in range(-10,10)]
# print("test_motor_speeds", test_motor_speeds)

test_servo_angles = [i*9 for i in range(-10,10)]
# print("test_servo_angles", test_servo_angles)

# motor1_speed = 0.75
# motor2_speed = -0.82
# motor3_speed = 0.344
# motor4_speed = -0.3149
# servo1_angle = 101
# servo2_angle = 82
# servo3_angle = 3
# servo4_angle = 21


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser2.flush()

    # test code
    i = -1

    while True:
        # test code
        i += 1
        i = i % 20
        motor1_speed = test_motor_speeds[i]
        motor2_speed = test_motor_speeds[i]
        motor3_speed = test_motor_speeds[i]
        motor4_speed = test_motor_speeds[i]
        servo1_angle = test_servo_angles[i]
        servo2_angle = test_servo_angles[i]
        servo3_angle = test_servo_angles[i]
        servo4_angle = test_servo_angles[i]


        arduino1_message = "<"+str(motor1_speed)+","+str(motor2_speed)+","+str(motor3_speed)+">"
        ser.write(bytes(arduino1_message))
        line = ser.readline().decode('utf-8').rstrip()
        print("Arduino 1 says: " + str(line))

        arduino2_message = "<"+str(motor4_speed)+","+str(servo1_angle)+","+str(servo2_angle)+","+str(servo3_angle)+","+str(servo4_angle)+">"
        ser2.write(bytes(arduino2_message))
        line = ser2.readline().decode('utf-8').rstrip()
        print("Arduino 2 says: " + str(line))

        time.sleep(timeout)