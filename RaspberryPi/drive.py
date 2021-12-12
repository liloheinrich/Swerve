import numpy as np
import math

def getsign(m):
    if m >= 0.0:
        return 1
    return -1

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

x_rot_bymodule = np.divide([1,1,-1,-1], math.sqrt(2.0))
y_rot_bymodule = np.divide([1,-1,-1,1], math.sqrt(2.0))
 
 
# inputs:
#   x_s - left joystick x-axis value on range [-1.0, 1.0]
#   y_s - left joystick y-axis value on range [-1.0, 1.0]
#   r_s - right joystick x-axis value on range [-1.0, 1.0]
#
# outputs:
#   res_mag - resulting vector magnitudes aka motor speeds on range [-1.0, 1.0]
#   res_ang - resulting vector angles aka servo angles, int() on range [-90, 90]
#
def drive(x_s, y_s, r_s):
    # turn r_s into magnitude and angle
    r_dir = getsign(r_s)
    r_mag = abs(r_s)
    print("r_mag", r_mag)
 
    # calculate x and y scaled vector components of the rotation
    x_r = x_rot_bymodule * r_mag
    y_r = y_rot_bymodule * r_mag

    for i in range(4):
        print("rotation angle for module:", i, math.degrees(math.atan2(y_rot_bymodule[i], x_rot_bymodule[i])))
        print("rotation x and y for module:", i, x_r[i], y_r[i])

    if r_dir < 0: # flip rotation vectors if counterclockwise
        x_r *= -1
        y_r *= -1
    for i in range(4):
        if x_r[i] < 0:
            x_r[i] = math.radians(180 + math.degrees(x_r[i]))
        if y_r[i] < 0:
            y_r[i] = math.radians(180 + math.degrees(y_r[i]))

    print("x_r, y_r", x_r, y_r)
    for i in range(4):
        print("rotation angle for module:", i, math.degrees(x_r[i]), math.degrees(y_r[i]))
        print("angle of y_r / x_r:", i, math.degrees(math.atan2(y_r[i], x_r[i])))


 
    # add x and y vector components of translation and rotation together
    res_x = [x_s + n for n in x_r]
    res_y = [y_s + n for n in y_r]
 
    # convert x and y components to magnitude and angle
    res_mag = [math.sqrt(res_x[i]**2 + res_y[i]**2) for i in range(4)]
    print("res_mag_this one", res_mag)

    res_ang = [(math.atan2(res_y[i], res_x[i])) for i in range(4)]

    # res_ang_degrees = [round(math.degrees(res_ang[i])) for i in range(len(res_ang))]
    # print("res_ang_degrees", res_ang_degrees)
 
    # scale magnitudes back into -1.0 to 1.0 range in case
    if any([abs(r) > 1.0 for r in res_mag]):
        max_mag = max(res_mag)
        res_mag = [(m / max_mag) for m in res_mag]
 
    # scale angles back into -90 to 90 degree range - reverse motors if necessary
    if any([a > 90 for a in res_ang]):
        res_ang = [a - 180 for a in res_ang]
        res_mag = [-m for m in res_mag]
 
    # gives motor speed (-1.0 to 1.0), servo angle (-90 to 90 degrees)
    return res_mag, res_ang


# inputs:
#   x_s - left joystick x-axis value on range [-1.0, 1.0]
#   y_s - left joystick y-axis value on range [-1.0, 1.0]
#   r_s - right joystick x-axis value on range [-1.0, 1.0]
#
# outputs:
#   res_mag - resulting vector magnitudes aka motor speeds on range [0.0, 1.0]
#   res_ang - resulting vector angles aka servo angles, int() on range [-90, 90]
#   res_dir - resulting vector of wheel directions, with positive/negative as 1/-1
#
def drive_3outputs_version(x_s, y_s, r_s):
    # start by calculating x and y scaled vector components
    r_dir = getsign(r_s)
    r_mag = abs(r_s)
    x_r =  x_rot_bymodule * r_mag
    y_r =  y_rot_bymodule * r_mag
    if not r_dir: # flip the rotation vectors if ccw
        x_r *= -1
        y_r *= -1

    # xy vector addition on the rotate and stafe vectors
    res_x = [x_s + n for n in x_r]
    res_y = [y_s + n for n in y_r]

    # convert xy to magnitude and angle
    res_mag = [math.sqrt(res_x[i]**2 + res_y[i]**2) for i in range(4)]
    res_ang = [math.atan(res_y[i] / res_x[i]) for i in range(4)] # todo: fix x = 0 error

    # separate motor magnitude (speed) and direction (fwd/rev)
    res_dir = [getsign(m) for m in res_mag]
    res_mag = [abs(m) for m in res_mag]

    # scale magnitudes back into 0.0 - 1.0 range in case (1.0 should be max speed)
    if any([r > 1.0 for r in res_mag]):
        max_mag = max(res_mag)
        res_mag = [(m / max_mag) for m in res_mag]

    # scale angles back into -90 to 90 degree servo range - reverse motors if necessary
    if any([a > 90 for a in res_ang]):
        res_ang = [a - 180 for a in res_ang]
        res_dir = [-d for d in res_dir]

    # gives motor fwd/rev (1/-1), motor speed (0.0 to 1.0), servo angle (-90 to 90 degrees)
    return res_dir, res_mag, res_ang


res_mag, res_ang = drive(1,0,1)

print("res_ang", res_ang)
res_ang = [round(math.degrees(a)) for a in res_ang]
print("res_ang", res_ang)
print("res_mag", res_mag)
