# reads joystick info from the socket
# calculates the swerve math
# sends commands to both arduinos


import socket
import serial
import time
import math
from drive import drive

#TODO
wheel_speed_coefficient = 1.0

#TODO
servo_angle = 90
motor_speed = 0.0

# servo_angles_ranges = [[15,175], [13,178], [16,170], [7,175]]
servo_angles_ranges = [[8,173], [12,170], [11,167], [10,175]]

def mapRange(oldMin, oldMax, oldValue, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = ((oldValue - oldMin) * newRange / oldRange) + newMin
    return newValue


timeout = 0.1 # time to wait before sending next data
ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser1.flush()
ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser2.flush()



# waiting for message
while True:
    motor_speeds_arr = [motor_speed for i in range(4)]
    servo_angles_arr = [servo_angle for i in range(4)]

    for i in range(4):
        servo_angles_arr[i] = mapRange(0, 180, servo_angle, servo_angles_ranges[i][0], servo_angles_ranges[i][1]) # map 0 to 180 onto corrected range
                

    arduino1_message = "["+str(round(motor_speeds_arr[0], 3))+","+str(round(motor_speeds_arr[1], 3))+","+str(int(servo_angles_arr[0]))+","+str(int(servo_angles_arr[1]))+"]"
    print("message to arduino1", arduino1_message)
    ser1.write(bytes(arduino1_message))

    arduino2_message = "["+str(round(motor_speeds_arr[2], 3))+","+str(round(motor_speeds_arr[3], 3))+","+str(int(servo_angles_arr[2]))+","+str(int(servo_angles_arr[3]))+"]"
    print("message to arduino2", arduino2_message)
    ser2.write(bytes(arduino2_message))

    time.sleep(timeout)
  
conn.close() # Close connections