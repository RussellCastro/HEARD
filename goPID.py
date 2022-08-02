from djitellopy import tello
import time

drone = tello.Tello()
drone.connect()

dt = 0.1 #update period

x_pos = 0
y_pos = 0
z_pos = 0

xkP = 0.0
xkI = 0.0
xkD = 0.0

ykP = 0.0
ykI = 0.0
ykD = 0.0

zkP = 0.0
zkI = 0.0
zkD = 0.0

xI = 0.0
yI = 0.0
zI = 0.0

def reg_update():
    x_accel = drone.get_acceleration_x
    y_accel = drone.get_acceleration_y
    z_accel = drone.get_acceleration_z

    x_vel = x_accel * dt
    y_vel = y_accel * dt
    z_vel = z_accel * dt

    x_pos += 0.5 * x_accel * dt ** 2
    y_pos += 0.5 * y_accel * dt ** 2
    z_pos += 0.5 * z_accel * dt ** 2

def go_PID(x_set, y_set, z_set):
    x_error = x_set - x_pos
    xI += xkI * x_error * dt

    x_u = xkP * x_error #x effort
    + xI
    + xkD * x_error / dt

    y_error = y_set - y_pos
    yI += ykI * y_error * dt

    y_u = ykP * y_error #y effort
    + yI
    + ykD * y_error / dt

    z_error = z_set - z_pos
    xI += xkI * x_error * dt

    z_u = zkP * z_error #x effort
    + xI
    + zkD * z_error / dt

    drone.send_rc_control(round(x_u), round(y_u), round(z_u))
    
def main():
    keep_going = True

    while keep_going == True:
        reg_update()
        time.sleep(dt)