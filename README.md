# Tello-AI
An repository with fun AI code to test with Tello drone containing line following, autopilot controlled by signs, drone control by hand. All that powered by OpenCV and TensorFlow based on Python! Made by **@ukicomputers**
# drone_line_following
https://github.com/ukicomputers/Tello-AI/assets/84191191/f9019784-7e52-434a-a8f2-29ca9d8ec4dd
## Usage:
Connect your Tello drone via Wi-Fi. 3D print a file for mirror clip, glue mirror on clip, and put clip onto Tello. Put ONLY A4 PAPERS on ground in direction what we want and make sure that there is no gaps between. To get the matching color of direction, run calibrator.py, and adjust a HSV values with scroll bar to match third image in second window to be direction white, and backround black. Then stop program with `q`. The output value will be printed in terminal. Copy the last value, open editor for main.py, and replace already existing hsvValues list, on line 19. Save the file, put the drone at beggining of direction and run main.py
## Requirements:
`pip install cv2`
`pip install djitellopy`
## Working:
When drone gets image, OpenCV finds contour with hsvValues, and get the center of contour. Then drone goes slowly forward. If OpenCV detects that is center moved little bit left or right, code sends rc_control command to drone for the turning on the curve until contour gets back to center.
# drone_autopilot
https://github.com/ukicomputers/Tello-AI/assets/84191191/409c3867-41cf-427b-b54c-ca9cfdbf9479
## Usage:
Connect your Tello drone via Wi-Fi and run a main.py file. Circle images are located in ./circles, print with A4. Change the code with dimensions and place printed circles on height of school chair.
## Requirements:
`pip install cv2`
`pip install djitellopy`
## Working:
When drone gets image it checks with OpenCV is there any circles on the image. If it is, then it counts how there many are. For example if there is 2 circles, drone will go left in specific range.
## Detection:
![20230420_115502-min](https://github.com/ukicomputers/Tello-AI/assets/84191191/7754f2c3-611a-44a1-8446-8b1827850cb5)
# drone_hand_command
https://github.com/ukicomputers/Tello-AI/assets/84191191/cbf5d68d-5fde-4693-ad07-c6244f270dcd
## Usage:
Connect your Tello drone via Wi-Fi and run a main.py file.
## Requirements:
`pip install cv2`
`pip install djitellopy`
`pip install mediapipe`
`python -version = 2.8.0`
## Working:
When drone gets image, it uses mediapipe libary to detects how many fingers is open. USE ONLY RIGHT HAND. Left has a problem with palm. For example, if it detects 5 fingers, then drone will go back.
