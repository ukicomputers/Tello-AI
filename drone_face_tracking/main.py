from utils import *
import cv2

myDrone = initializeTello()
w, h = 360, 240
pid = [0.5, 0.5, 0]
pError = 0

started = 0

if started == 0:
    myDrone.takeoff()
    started = 1

while True:
    myDrone.send_read_command("command")

    img = telloGetFrame(myDrone, w, h)
    img, info = findFace(img)
    pError = trackFace(myDrone, info, w, pid, pError)

    cv2.imshow('Izlaz', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
