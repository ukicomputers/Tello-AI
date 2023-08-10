#Code written by ukicomputers. from literature for MediaPipe
import mediapipe as mp
import time
import cv2

class handDetector(): #klasa za detekciju
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5): #za pozivanje iz drugih fajlova
        #priprema variabla
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(self.detectionCon))
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw = True): #funkcija za pronalaženje ruku
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #menjanje boje slike
        self.results = self.hands.process(imgRGB) #detkcija koristeći MediaPipe

        if self.results.multi_hand_landmarks: #crtanje pronađenih znakova
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPostition(self, img, handNo = 0): #pronalazak pozicije ruku (output: [0, 0, 0, 0, 0])
        lmList = []
        if self.results.multi_hand_landmarks: #za pronađeno
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy]) #ubacivanje u listu
        return lmList