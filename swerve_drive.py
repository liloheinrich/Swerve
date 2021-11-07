import numpy as np
import math

x_rot = np.multiply([1,1,-1,-1], math.sqrt(2.0))
y_rot = np.multiply([1,-1,-1,1], math.sqrt(2.0))

def getsign(m):
    if m >= 0.0:
        return 1
    return -1

# drive() takes params describing desired driving movement, 
# outputs the direction, angle, and speed to set each module.
# 
# inputs:
#   s_dir = strafe direction (angle from 0 to 360),
#   s_mag = strafe magnitude (0.0 to 1.0 speed scalar),
#   r_dir = rotate direction (true = cw, false = ccw),
#   r_mag = rotate magnitude (0.0 to 1.0 speed scalar)
# 
# returns: 
#   motor fwd/rev (1/-1),
#   motor speed (0.0 to 1.0), 
#   servo angle (0.0 to 180.0 degrees) 
def drive(s_dir, s_mag, r_dir, r_mag):
    # start by calculating x and y scaled vector components
    x_s = math.sin(s_dir) * s_mag * math.sqrt(2.0)
    y_s = math.cos(s_dir) * s_mag * math.sqrt(2.0)
    x_r = x_rot * r_mag
    y_r = y_rot * r_mag
    if not r_dir: # flip the rotation vectors if ccw
        x_r *= -1
        y_r *= -1
    
    # xy vector addition on the rotate and stafe vectors
    res_x = [x_s + n for n in x_r]
    res_y = [y_s + n for n in y_r]

    # convert xy to magnitude and angle
    res_mag = [[math.sqrt(x * x + y * y) for x in res_x] for y in res_y]
    res_ang = [[math.tan(y, x) for x in res_x] for y in res_y]

    # separate motor magnitude (speed) and direction (fwd/rev)
    res_dir = [getsign(m) for m in res_mag]
    res_mag = [math.abs(m) for m in res_mag]

    # scale magnitudes back into 0.0 - 1.0 range in case (1.0 should be max speed)
    if res_mag.any() > 1.0:
        max_mag = max(res_mag)
        res_mag = [(m / max_mag) for m in res_mag]

    # scale angles back into 180 degree servo range - reverse motors if necessary
    if res_ang.any() > 180.0:
        res_ang = [a - 180.0 for a in res_ang]
        res_dir = [-d for d in res_dir]

    # gives motor fwd/rev (1/-1), motor speed (0.0 to 1.0), servo angle (0.0 to 180.0 degrees)
    return res_dir, res_mag, res_ang