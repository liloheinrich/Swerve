# reads joystick info from the socket
# calculates the swerve math
# sends commands to both arduinos

import socket
import serial
import time
import math
from drive import drive

# square to circle joystick correction
# https://www.xarg.org/2017/07/how-to-map-a-square-to-a-circle/
def map(x, y):
    return x * math.sqrt(1 - y*y/2.0), y * math.sqrt(1 - x*x/2.0)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

wheel_speed_coefficient = 1.0
servo_angles_ranges = [[8,173], [12,170], [11,167], [10,175]]

def mapFromTo(x,a,b,c,d):
    # x:input value; 
    # a,b:input range
    # c,d:output range
   return int((x-a)/(b-a)*(d-c)+c)


def mapRange(oldMin, oldMax, oldValue, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = ((oldValue - oldMin) * newRange / oldRange) + newMin
    return newValue

deadband = 0.01
# default_joyvalue = -256
max_joyvalue = 32768

# HOST = '' # Server IP or Hostname
HOST = '10.3.141.1'
print("HOST = ", HOST)
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#managing error exception
try:
  s.bind((HOST, PORT))
except socket.error:
  print('Bind failed')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')

timeout = 0.1 # time to wait before sending next data
ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser1.flush()
ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser2.flush()

# waiting for message
while True:
    data = conn.recv(1024)
    # print('Data: ' + data) 

    if data == 'quit':
        conn.send('Terminating')
        break
    conn.send('Received')
    # print("data received", data)
    data = data.strip("[").strip("]")

    if len(data) > 0:

        joystick_readings = [float(i) for i in data.split(",")]
        # print("joystick_readings", joystick_readings)

        # x_s, y_s, r_s = 0.0, 0.0, 0.0
        motor_speeds_arr = [0.0 for i in range(4)]
        servo_angles_arr = [0 for i in range(4)]

        servo_angle = 90
        motor_speed = 0.0
        if any([abs(v) > deadband for v in joystick_readings[0:3]]):
            # print("axis:", joystick_readings)

            motor_speed = joystick_readings[2]
            if abs(joystick_readings[0]) > deadband or abs(joystick_readings[1]) > deadband:
                servo_angle = 180 - math.degrees(math.atan2(-joystick_readings[1], joystick_readings[0])) # range: -90 to 90
            else:
                servo_angle = 90

        for i in range(4):
            # convert servo angles to the right range
            if servo_angle > 180:
                servo_angles_arr[i] = mapRange(0, 180, servo_angle%180, servo_angles_ranges[i][0], servo_angles_ranges[i][1]) # map 0 to 180 onto corrected range
                motor_speeds_arr[i] = -motor_speed
            else:
                motor_speeds_arr[i] = motor_speed
                servo_angles_arr[i] = mapRange(0, 180, servo_angle, servo_angles_ranges[i][0], servo_angles_ranges[i][1]) # map 0 to 180 onto corrected range
                
        # print("motor_speeds_arr", motor_speeds_arr)
        # print("servo_angles_arr", servo_angles_arr)

        arduino1_message = "["+str(round(motor_speeds_arr[0], 3))+","+str(round(motor_speeds_arr[1], 3))+","+str(int(servo_angles_arr[0]))+","+str(int(servo_angles_arr[1]))+"]"
        print("message to arduino1", arduino1_message)
        ser1.write(bytes(arduino1_message))


        arduino2_message = "["+str(round(motor_speeds_arr[2], 3))+","+str(round(motor_speeds_arr[3], 3))+","+str(int(servo_angles_arr[2]))+","+str(int(servo_angles_arr[3]))+"]"
        print("message to arduino2", arduino2_message)
        ser2.write(bytes(arduino2_message))

    else:
        print("Data had len < 0", data)

    # line = ser1.readline().decode('utf-8') #.rstrip()
    # print("arduino returns " + str(line))
    # line = ser1.readline().decode('utf-8') #.rstrip()
    # print("arduino returns " + str(line))

    time.sleep(timeout)
  
conn.close() # Close connections