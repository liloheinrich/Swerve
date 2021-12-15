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

#TODO
wheel_speed_coefficient = 0.8

#TODO
servo_angles_ranges = [[8,173], [12,170], [11,167], [10,175]]

def mapRange(oldMin, oldMax, oldValue, newMin, newMax):
    oldRange = (oldMax - oldMin)
    newRange = (newMax - newMin)
    newValue = ((oldValue - oldMin) * newRange / oldRange) + newMin
    return int(newValue)

deadband = 0.01

# HOST = '' # Server IP or Hostname
# HOST = socket.gethostname()
HOST = '10.3.141.1'
print("HOST = ", HOST)
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

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

prev_res_ang = [i[0] for i in servo_angles_ranges]

# waiting for message
while True:
    data = conn.recv(1024)
    # print('Data: ' + data) 

    if data == 'quit':
        conn.send('Terminating')
        break
    conn.send('Received')
    data = data.strip("[").strip("]")

    if len(data) > 0:
        joystick_readings = [float(i) for i in data.split(",")]
        # print("joystick_readings", joystick_readings)

        x_s, y_s, r_s = 0.0, 0.0, 0.0
        motor_speeds_arr = [0.0 for i in range(4)]
        servo_angles_arr = [0 for i in range(4)]

        if any([abs(v) > deadband for v in joystick_readings[0:3]]):
            x_s = joystick_readings[0]
            y_s = joystick_readings[1]
            r_s = joystick_readings[2]
            # print("x_s, y_s, r_s", x_s, y_s, r_s)

            res_mag, res_ang = drive(x_s, y_s, r_s)
            res_mag = [round(r, 3) for r in res_mag]
            res_ang = [round(math.degrees(a)) for a in res_ang]
            # print("res_mag", res_mag)
            # print("res_ang", res_ang)
            prev_res_ang = res_ang
        else:
            res_ang = prev_res_ang
            res_mag = [0.0 for i in range(4)]

        res_ang = [res_ang[0], res_ang[3], res_ang[1], res_ang[2]]
        for i in range(4):

            res_ang[i] += 180
            if res_ang[i] > 180:
                servo_angles_arr[i] = mapRange(0, 180, res_ang[i]%180, servo_angles_ranges[i][0], servo_angles_ranges[i][1]) # map 0 to 180 onto corrected range
                motor_speeds_arr[i] = -res_mag[i] * wheel_speed_coefficient
            else:
                motor_speeds_arr[i] = res_mag[i] * wheel_speed_coefficient
                servo_angles_arr[i] = mapRange(0, 180, res_ang[i], servo_angles_ranges[i][0], servo_angles_ranges[i][1]) # map 0 to 180 onto corrected range
            
        arduino1_message = "["+str(motor_speeds_arr[0])+","+str(motor_speeds_arr[1])+","+str(servo_angles_arr[0])+","+str(servo_angles_arr[1])+"]"
        # print("arduino1_message", arduino1_message)
        ser1.write(bytes(arduino1_message))
        arduino2_message = "["+str(motor_speeds_arr[2])+","+str(motor_speeds_arr[3])+","+str(servo_angles_arr[2])+","+str(servo_angles_arr[3])+"]"
        # print("arduino2_message", arduino2_message)
        ser2.write(bytes(arduino2_message))

    else:
        print("Data had len < 0", data)

    # line = ser1.readline().decode('utf-8') #.rstrip()
    # print("arduino returns " + str(line))
    # line = ser1.readline().decode('utf-8') #.rstrip()
    # print("arduino returns " + str(line))

    time.sleep(timeout)
  
conn.close() # Close connections