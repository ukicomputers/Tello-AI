import detector
import cv2
from djitellopy import Tello
import time

takeoff = 0
w, h = 640, 480

dron = Tello()
dron.connect()

dron.streamoff()
dron.streamon()

print(dron.get_battery())

if takeoff == 0:
    dron.takeoff()
    #dron.move_up(25)
    takeoff = 1

while True:
    frame_read = dron.get_frame_read()
    frame = frame_read.frame
    img = cv2.resize(frame, (w, h))

    detected = detektor.detekcija(img)
    
    if detected[1] == 1:
        dron.rotate_counter_clockwise(90)
        time.sleep(1)
    elif detected[1] == 6:
        dron.move_left(100)
        time.sleep(1)
    elif detected[1] == 3:
        dron.rotate_counter_clockwise(180)
        time.sleep(1)
    elif detected[1] == 5:
        dron.move_left(100)
        time.sleep(1)
    elif detected[1] == 2:
        dron.rotate_counter_clockwise(90)
        time.sleep(3)
        dron.land()
        break

    cv2.imshow('izlaz', detected[0])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        dron.land()
        break
