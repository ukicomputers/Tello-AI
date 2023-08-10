#written by ukicomputers.

#importovanje biblioteka
import cv2
import numpy as np

def detekcija(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #pretvaramo sliku u sive nijanse
	gray = cv2.blur(gray, (3, 3)) #izravnjavamo sliku koristeci zamucenje
	
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
				   param1 = 50, param2 = 30,
				   minRadius = 1, maxRadius = 35) #detektovanje krugova

	i = 0 #brojac za detektovane krugove

	if circles is not None: #ako su pronadjeni
		circles = np.uint16(np.around(circles)) #x, y, radijus kruga
		
		for pt in circles[0, :]: #slikovito prikazivanje i brojanje krugova
			x, y, r = pt[0], pt[1], pt[2]
			cv2.circle(img, (x, y), r, (0, 255, 0), 2)
			cv2.circle(img, (x, y), 1, (0, 0, 255), 3)
			i = i + 1

	return [img, i]
