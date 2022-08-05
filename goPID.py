from djitellopy import tello
import time, cv2

drone = tello.Tello()
drone.connect()
drone.streamon()

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
focal = 12096.75

x_center = 0.0
y_dist = 0.0 #dist from locator tag

dt = 0.1 #update period

x_pos = 0.0
y_pos = 0.0
z_pos = 0.0

xkP = 0.10
xkI = 0.0
xkD = 0.0

ykP = 0.003
ykI = 0.0
ykD = 0.0

zkP = 0.3
zkI = 0.0
zkD = 0.05

xI = 0.0
yI = 0.0
zI = 0.0

def reg_update(): #state update process
    #positional update
    global x_pos
    global y_pos
    global z_pos
    global x_center

    z_pos = drone.get_barometer() #barometer units
    print('x pos: ' + str(x_center))
    print('y pos: ' + str(y_pos))
    print('z pos: ' + str(z_pos))

    #stream update; tello res: 1280x720
    img = drone.get_frame_read().frame
    corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    detection = cv2.aruco.drawDetectedMarkers(img, corners, borderColor=(255,0,0))
    cv2.imshow('stream', detection)
    cv2.imshow('detection', detection)
    try:
        cv2.waitKey(1)
        real_corners = corners[0]
        x_size = abs(real_corners[0,0,0] - real_corners[0,2,0])
        y_dist = focal / x_size
        y_pos = y_dist
        x_center = (real_corners[0,0,0] + real_corners[0,2,0]) / 2
    except:
        pass

#PID relative to tag
def doTagPID(z_set, x_set=640, y_set=20):
    global xI, yI, zI
    x_error = x_set - x_center
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

    z_u = zkP * z_error #z effort
    + xI
    + zkD * z_error / dt

    print('x effort: ' + str(round(x_u)))
    print('y effort: ' + str(round(y_u)))
    print('z effort: ' + str(round(z_u)))

    drone.send_rc_control(round(x_u), 0, 0, 0) #, round(z_u)

def goPID():
    drone.takeoff()
    #drone.move_up(20)
    keep_going = True

    while keep_going == True:
        reg_update()
        doTagPID(1000)
        time.sleep(dt)

goPID()

# def doPID(x_set, y_set, z_set):
#     global xI, yI, zI
#     x_error = x_set - x_pos
#     xI += xkI * x_error * dt

#     x_u = xkP * x_error #x effort
#     + xI
#     + xkD * x_error / dt

#     y_error = y_set - y_pos
#     yI += ykI * y_error * dt

#     y_u = ykP * y_error #y effort
#     + yI
#     + ykD * y_error / dt

#     z_error = z_set - z_pos
#     xI += xkI * x_error * dt

#     z_u = zkP * z_error #z effort
#     + xI
#     + zkD * z_error / dt

#     print('x effort: ' + str(round(x_u)))
#     print('y effort: ' + str(round(y_u)))
#     print('z effort: ' + str(round(z_u)))

#     drone.send_rc_control(0, 0, round(z_u), 0) #, round(z_u)