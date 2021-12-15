import numpy as np
import math
# from visualize import add_vectors, visualize

def getsign(m):
    if m >= 0.0:
        return 1
    return -1

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

x_rot_bymodule = np.divide([-1,-1,1,1], math.sqrt(2.0))
y_rot_bymodule = np.divide([-1,1,1,-1], math.sqrt(2.0))
 
x_rot_bymodule *= -1
y_rot_bymodule *= -1
 
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
 
    # calculate x and y scaled vector components of the rotation
    x_r = x_rot_bymodule * r_mag
    y_r = y_rot_bymodule * r_mag

    # add_vectors(x_r, y_r, (0,0,0))

    if r_dir < 0: # flip rotation vectors if counterclockwise
        x_r *= -1
        y_r *= -1

    # add_vectors(x_r, y_r, (255,0,0))
    # add_vectors([x_s for i in range(4)], [y_s for i in range(4)], (0,0,255))
 
    # add x and y vector components of translation and rotation together
    res_x = [x_s + x_r[i] for i in range(len(x_r))]
    res_y = [y_s + y_r[i] for i in range(len(y_r))]

    # add_vectors(res_x, res_y, (0,255,0))
 
    # convert x and y components to magnitude and angle
    res_mag = [math.sqrt(res_x[i]**2 + res_y[i]**2) for i in range(4)]
    res_ang = [(math.atan2(res_y[i], res_x[i])) for i in range(4)]

    # scale magnitudes back into -1.0 to 1.0 range in case
    if any([abs(r) > 1.0 for r in res_mag]):
        max_mag = max(res_mag)
        res_mag = [(m / max_mag) for m in res_mag]
 
    # scale angles back into -90 to 90 degree range - reverse motors if necessary
    if any([a > 90 for a in res_ang]):
        res_ang = [a - 180 for a in res_ang]
        res_mag = [-m for m in res_mag]

    # visualize()
 
    # gives motor speed (-1.0 to 1.0), servo angle (-90 to 90 degrees)
    return res_mag, res_ang

# res_mag, res_ang = drive(1,0,1)
# res_ang = [round(math.degrees(a)) for a in res_ang]
# print("res_ang", res_ang)
# print("res_mag", res_mag)