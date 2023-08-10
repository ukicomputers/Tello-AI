import cv2
import numpy as np
from djitellopy import Tello

dron = Tello()
dron.connect()
print(dron.get_battery())

dron.takeoff()
dron.move_down(45)

dron.streamoff()
dron.streamon()

w, h = 480, 360

#hsvValues = [75, 72, 122, 179, 255, 255] #svetlo plava traka
#hsvValues = [45, 0, 23, 179, 255, 255] #tamno plava traka
hsvValues = [0, 0, 188, 179, 33, 245] #beli papir

sensors = 3
theresholdNum = 0.2
sensitivity = 3
fSpeed = 7

weights = [-25, -15, 0, 15, 25]
curve = 0

def thereshold(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvValues[0], hsvValues[1], hsvValues[2]])
    upper = np.array([hsvValues[3], hsvValues[4], hsvValues[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getContours(imgTh, img):
    cx = 0
    cy = 0
    contours, hierarchy = cv2.findContours(imgTh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgTh, sensors):
    imgs = np.hsplit(imgTh, sensors)
    totalPixels = (img.shape[1] // sensors) * img.shape[0]
    senOut = []

    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)

        if pixelCount > theresholdNum * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)

    return senOut


def sendCommand(senOut, cx):
    global curve

    lr = (cx - w // 2) // sensitivity
    lr = int(np.clip(lr, -10, 10))
    if lr < 2 and lr > -2: lr = 0

    if senOut == [1, 0, 0]:
        curve = weights[0]
    elif senOut == [1, 1, 0]:
        curve = weights[1]
    elif senOut == [0, 1, 0]:
        curve = weights[2]
    elif senOut == [0, 1, 1]:
        curve = weights[3]
    elif senOut == [0, 0, 1]:
        curve = weights[4]
    elif senOut == [0, 0, 0]:
        curve = weights[2]
    elif senOut == [1, 1, 1]:
        curve = weights[2]
    elif senOut == [1, 0, 1]:
        curve = weights[2]

    """if lr > 0 or lr < 0:
        dron.send_rc_control(lr, 0, 0, curve)
    else:
        dron.send_rc_control(lr, fSpeed, 0, curve)"""
    
    dron.send_rc_control(lr, fSpeed, 0, curve)


while True:
    img = dron.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img = cv2.flip(img, 0)

    imgTh = thereshold(img)
    cx = getContours(imgTh, img)
    senOut = getSensorOutput(imgTh, sensors)
    sendCommand(senOut, cx)

    cv2.imshow("izlaz", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        dron.land()
        break
    
