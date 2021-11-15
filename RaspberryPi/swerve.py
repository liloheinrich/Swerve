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

deadband = 500
# default_joyvalue = -256
max_joyvalue = 32768

# HOST = '' # Server IP or Hostname
# HOST = socket.gethostname()
# HOST = '10.27.91.11'
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
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser2.flush()

# waiting for message
while True:
    data = conn.recv(1024)
    print('Data: ' + data) 

    if data == 'quit':
        conn.send('Terminating')
        break
    conn.send('Received')

    joystick_readings = [float(i) for i in data.split(",")]
    print("joystick_readings", joystick_readings)

    x_s, y_s, r_s = 0.0, 0.0, 0.0
    if any([abs(v) > deadband for v in joystick_readings[0:3]]):
        # print("axis:", joystick_readings)

        x_s_raw = clamp(joystick_readings[0] / max_joyvalue, -1.0, 1.0)
        y_s_raw = clamp(joystick_readings[1] / max_joyvalue, -1.0, 1.0)
        r_s = clamp(joystick_readings[2] / max_joyvalue, -1.0, 1.0)
        x_s, y_s = map(x_s_raw, y_s_raw)
        # print("x_s, y_s, r_s", round(x_s, 4), round(y_s, 4), round(r_s, 4))

    res_mag, res_ang = drive(x_s, y_s, r_s)
    res_mag = [round(r, 3) for r in res_mag]
    res_ang = [round(math.degrees(a)) for a in res_ang]
    print("res_mag, res_ang", res_mag, res_ang)

    # arduino1_message = res_mag[0:2].__str__()
    # print(arduino1_message)
    arduino1_message = "["+str(res_mag[1])+","+str(res_mag[2])+","+str([3])+"]"
    ser.write(bytes(arduino1_message))
    line = ser.readline().decode('utf-8').rstrip()
    print("Arduino 1 says: " + str(line))

    # arduino2_message = "[" + res_mag[3] + "," + res_ang.__str__()[1:]
    # print(arduino2_message)
    arduino2_message = "["+str(res_mag[3])+","+str(res_ang[0])+","+str(res_ang[1])+","+str(res_ang[2])+","+str(res_ang[3])+"]"
    ser2.write(bytes(arduino2_message))
    line = ser2.readline().decode('utf-8').rstrip()
    print("Arduino 2 says: " + str(line))

    time.sleep(timeout)
  
conn.close() # Close connections