# the pi is meant to be the server, the laptop the client
# https://coderedirect.com/questions/597581/how-to-get-usb-controller-gamepad-to-work-with-python

import joystickapi
import time

# 0: select 
# 1: left joystick press
# 2: right joystick press
# 3: start
# 4: dpad up
# 5: dpad right
# 6: dpad down
# 7: dpad left
# 8: right joystick press
# 9: left trigger
# 10: right trigger
# 11: left bumper
# 12: right bumper
# 13: green triangle up
# 14: red circle right
# 15: blue x down
# 16: purple square left
# 17: middle button clear

# axis 0/X: left joystick R-L axis
# axis 1/Y: left joystick up-down axis
# axis 2/Z: right joystick R-L axis
# axis 3/R: right joystick up-down axis


# the pi is meant to be the server, the laptop the client
# Level 1: https://raspberrypi.stackexchange.com/questions/13425/server-and-client-between-pc-and-raspberry-pi
# Level 2: https://notenoughtech.com/raspberry-pi/rpi-socket-protocol/
# Level 3: http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php

import socket

HOST = '10.27.91.11' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

print("start")
deadband = 500
# default_joyvalue = -256
max_joyvalue = 32768
rate = 0.1 # sleep between loops in seconds

num = joystickapi.joyGetNumDevs()
ret, caps, startinfo = False, None, None
for id in range(num):
    ret, caps = joystickapi.joyGetDevCaps(id)
    if ret:
        print("gamepad detected: " + caps.szPname)
        ret, startinfo = joystickapi.joyGetPosEx(id)
        break
else:
    print("no gamepad detected")



# todo: might want to do more with timing, ex loop timing or time/duration of/between readings
run = ret # todo: make loop start and stop upon certain buttons
while run:
    time.sleep(rate)

    ret, info = joystickapi.joyGetPosEx(id)
    if ret:
        btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)][0:17]
        axisXYZR = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos, info.dwRpos-startinfo.dwRpos]
        if info.dwButtons:
            print("buttons: ", btns)
        if any([abs(v) > deadband for v in axisXYZR[0:3]]):
            print("axis:", axisXYZR)
        # else:
            # print("inactive, under deadband")

        s.send(str.encode(str(btns) + str(axisXYZR)))
        reply = s.recv(1024).decode()
        if reply == 'Terminate':
            break
        print(reply)

        # todo: this is where the sending code would go
        # use sockets
        # https://stackoverflow.com/questions/59853852/sending-data-from-pc-to-raspberry-pi-using-python
    # todo: re^: or here for a const hz rate, not too sure...

print("end")