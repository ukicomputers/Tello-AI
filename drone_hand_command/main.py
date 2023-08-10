#Code written by ukicomputers. from literature for MediaPipe (see line 25)
import cv2
import os
import ukicomputers.HandTrackingModule as htm
from djitellopy import Tello
import time

width, height = 640, 480 #postavka dužine i visine

#povezivanje na dron
dron = Tello()
dron.connect()

#uključivanje prenosa slike
dron.streamoff()
dron.streamon()

print(dron.get_battery())

#priprema ilustrativnih slika (koliko je prstiju pokazano)
folderPath = "FingerImages"
directoryFileList = os.listdir(folderPath)

#isto, samo čitanje njih i ubacivanje u listu
pictureList = []
for imPath in directoryFileList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    pictureList.append(image)

takeoff = 0 #variabla za poletanje. stavite na 1 ukoliko ne želite da dron poleti.
detector = htm.handDetector(detectionCon = 0.75) #priprema detektora za ruke
fingerIds = [4, 8, 12, 16, 20] #literatura: https://google.github.io/mediapipe/solutions/hands.html

detected = 0

if takeoff == 0:
    dron.takeoff()
    takeoff = 1

while True:
    time.sleep(1)
    frame_read = dron.get_frame_read() #dobijanje frame-a iz kamere sa drona
    frame = frame_read.frame #postavka
    img = cv2.resize(frame, (width, height)) #resize
    
    img = detector.findHands(img) #pronalazi ruke koristeći MediaPipe
    lmList = detector.findPostition(img) #dobija informacije na kojoj su poziciji prsti

    if len(lmList) != 0: #stavljanje u listu za detekciju
        fingers = []

        #Palac
        if lmList[fingerIds[0]][1] > lmList[fingerIds[0] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #Ostala četri prsta
        for id in range(1, 5):
            if lmList[fingerIds[id]][2] < lmList[fingerIds[id] - 1][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1) #ukupno prstiju (sabiranje)

        #prikazivanje slike i resize
        h, w, c = pictureList[totalFingers - 1].shape
        img[0:h, 0:w] = pictureList[totalFingers - 1]

        #final touch, broj detektovanih prstiju na izlaznoj slici
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

        #kontrola drona po detekciji
        if totalFingers == 0:
            dron.move("forward", 50)
            time.sleep(1)
        elif totalFingers == 1:
            dron.move("up", 50)
            time.sleep(1)
        elif totalFingers == 2:
            dron.move("down", 50)
            time.sleep(1)
        elif totalFingers == 3:
            dron.move("left", 50)
            time.sleep(1)
        elif totalFingers == 4:
            dron.move("right", 50)
            time.sleep(1)
        elif totalFingers == 5:
            dron.move("back", 50)
            time.sleep(1)
        
    cv2.imshow("Izlaz", img)

    dron.send_read_command("command")
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #ukoliko se pritisne na tastaturi slovo Q, program će se zaustaviti
        dron.land()
        break
