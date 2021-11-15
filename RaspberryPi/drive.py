import numpy as np
import math

x_rot = np.divide([1,1,-1,-1], math.sqrt(2.0))
y_rot = np.divide([1,-1,-1,1], math.sqrt(2.0))

def getsign(m):
    if m >= 0:
        return 1
    return -1


# like drive_vector, expect it takes x_s x-strafe component from
# from -1.0 to 1.0, and y_s y-strafe component from -1.0 to 1.0, 
# and rotate as a signed value rather than r_dir and r_mag.
# meant to interface with joystick axes easily.
def drive(x_s, y_s, r_s):
    # start by calculating x and y scaled vector components
    r_dir = getsign(r_s)
    r_mag = abs(r_s)
    x_r = x_rot * r_mag
    y_r = y_rot * r_mag
    if not r_dir: # flip the rotation vectors if ccw
        x_r *= -1
        y_r *= -1

    # xy vector addition on the rotate and stafe vectors
    res_x = [x_s + n for n in x_r]
    res_y = [y_s + n for n in y_r]

    # convert xy to magnitude and angle
    res_mag = [math.sqrt(res_x[i]**2 + res_y[i]**2) for i in range(4)]
    res_ang = [math.atan(res_y[i] / res_x[i]) for i in range(4)] # todo: fix x = 0 error

    # # separate motor magnitude (speed) and direction (fwd/rev)
    # res_dir = [getsign(m) for m in res_mag]
    # res_mag = [abs(m) for m in res_mag]

    # scale magnitudes back into -1.0 to 1.0 range in case (1.0 should be max speed)
    if any([abs(r) > 1.0 for r in res_mag]):
        max_mag = max(res_mag)
        res_mag = [(m / max_mag) for m in res_mag]

    # scale angles back into -90 to 90 degree servo range - reverse motors if necessary
    if any([a > 90 for a in res_ang]):
        res_ang = [a - 180 for a in res_ang]
        res_mag = [-m for m in res_mag]

    # gives motor speed (-1.0 to 1.0), servo angle (-90 to 90 degrees)
    return res_mag, res_ang


# drive() takes params describing desired driving movement, 
# outputs the direction, angle, and speed to set each module.
# 
# inputs:
#   s_dir = strafe direction (angle from -90 to 90),
#   s_mag = strafe magnitude (0.0 to 1.0 speed scalar),
#   r_dir = rotate direction (true = cw, false = ccw),
#   r_mag = rotate magnitude (0.0 to 1.0 speed scalar)
# 
# returns: 
#   motor fwd/rev (1/-1),
#   motor speed (0.0 to 1.0), 
#   servo angle (-90 to 90 degrees) 
def drive_vector(s_dir, s_mag, r_dir, r_mag):
    # start by calculating x and y scaled vector components
    x_s = math.sin(s_dir) * s_mag / math.sqrt(2.0)
    y_s = math.cos(s_dir) * s_mag / math.sqrt(2.0)
    x_r = x_rot * r_mag
    y_r = y_rot * r_mag
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


# like drive_vector, expect it takes x_s x-strafe component from
# from -1.0 to 1.0, and y_s y-strafe component from -1.0 to 1.0, 
# and rotate as a signed value rather than r_dir and r_mag.
# meant to interface with joystick axes easily.
def drive_with_sep_dir(x_s, y_s, r_s):
    # start by calculating x and y scaled vector components
    r_dir = getsign(r_s)
    r_mag = abs(r_s)
    x_r = x_rot * r_mag
    y_r = y_rot * r_mag
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