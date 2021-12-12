# https://coderedirect.com/questions/597581/how-to-get-usb-controller-gamepad-to-work-with-python

from drive import drive
import joystickapi
import time
import math

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


# square to circle joystick correction
# https://www.xarg.org/2017/07/how-to-map-a-square-to-a-circle/
def map(x, y):
    return x * math.sqrt(1 - y*y/2.0), y * math.sqrt(1 - x*x/2.0)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

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

run = ret
while run:
    time.sleep(rate)
    ret, info = joystickapi.joyGetPosEx(id)
    if ret:
        btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)][0:17]
        axisXYZR = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos, info.dwRpos-startinfo.dwRpos]
        if info.dwButtons:
            print("buttons: ", btns)
        if any([abs(v) > deadband for v in axisXYZR[0:3]]):
            # print("axis:", axisXYZR)

            x_s_raw = clamp(axisXYZR[0] / max_joyvalue, -1.0, 1.0)
            y_s_raw = clamp(axisXYZR[1] / max_joyvalue, -1.0, 1.0)
            r_s = clamp(axisXYZR[2] / max_joyvalue, -1.0, 1.0)
            x_s, y_s = map(x_s_raw, y_s_raw)
            # print("x_s, y_s, r_s", round(x_s, 4), round(y_s, 4), round(r_s, 4))

            res_dir, res_mag, res_ang = drive(x_s, y_s, r_s)
            res_mag = [round(r, 3) for r in res_mag]
            res_ang = [round(math.degrees(a), 1) for a in res_ang]
            print("res_dir, res_mag, res_ang", res_dir, res_mag, res_ang)

        else:
            print("inactive, under deadband")

print("end")