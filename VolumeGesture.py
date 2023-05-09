import cv2
import time
import numpy as np
import ctypes
import HandTrackingModule as htm
import math
import osascript

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.5)

minVol = 0
maxVol = 100
vol=0
volBar=400
pTime=0
while True:

    success,img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])

        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]

        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        #print(length)
        #hand range 20-300
        #volume range 0-100

        vol = np.interp(length,[30,300],[0,100])
        volBar = np.interp(length, [30, 300], [400, 150])

        print(vol)

        vol1 = "set volume output volume " + str(int(vol))
        osascript.osascript(vol1)

        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(vol))+" %", (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)
