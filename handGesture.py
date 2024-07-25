import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import cv2

def hand_gesture():
    camWidth, camHeight = 1200, 720
    imgNo = 0
    pptCamHeight, pptCamWidth = int(camHeight/4*0.8), int(camWidth/4*0.8)
    detectionThreshold = 300
    gestureDetected = False
    gestureCounter = 0
    gestureDelay = 30
    annotations = [[]]
    annotationNumber = 0
    annotationStart = False
    folderPath = r"C:\Users\ky040\OneDrive\Desktop\PowerPoint-Generator-Python-Project-main\PowerPoint-Generator-Python-Project-main\uploads\Slides"
    # get the list of images of the presentation
    images = sorted(os.listdir(folderPath), key=len)
    # Hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # setting up the camera
    videoCapture = cv2.VideoCapture(0)
    videoCapture.set(3, camWidth)
    videoCapture.set(4, camHeight)

    # gestures
    while True:
        success, img = videoCapture.read()
        # 0=vertical 1= horizontal
        img = cv2.flip(img, 1)
        fullPath = os.path.join(folderPath, images[imgNo])
        currImage = cv2.imread(fullPath)
        
        cv2.line(img, (0, detectionThreshold), (camWidth, detectionThreshold), (0, 255, 0), 10)
        # hands, img = detector.findHands(img, flipType=False) for left and right
        hands, img = detector.findHands(img)

        if hands and gestureDetected is False:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            centerxppt, centeryppt = hand['center']
            lmList = hand['lmList']

            # Constraints for easier navigation
            indexFinger = lmList[8][0], lmList[8][1]
            xVal = int(np.interp(lmList[8][0], [camWidth//2, camWidth], [0, camWidth]))
            yVal = int(np.interp(lmList[8][1], [150, camHeight - 400], [0, camHeight]))
            indexFinger = xVal, yVal

            if centeryppt <= detectionThreshold:
                # 1st gesture
                if fingers == [1, 0, 0, 0, 0]:
                    annotationStart = False
                    print("left")
                    if imgNo > 0:
                        gestureDetected = True
                        annotations = [[]]
                        annotationNumber = 0
                        imgNo -= 1
                # 2nd gesture
                if fingers == [0, 0, 0, 0, 1]:
                    annotationStart = False
                    print("right")
                    if imgNo < len(images)-1:
                        gestureDetected = True
                        annotations = [[]]
                        annotationNumber = 0
                        imgNo += 1
            # 3rd gesture
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(currImage,indexFinger, 12, (0,0,255), cv2.FILLED)
                annotationStart = False

            # 4th gesture
            if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                cv2.circle(currImage, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                annotations[annotationNumber].append(indexFinger)
            else:
                annotationStart = False

            # 5th gesture
            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    if annotationNumber >= 0:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        gestureDetected = True

        else:
            annotationStart = False

        if gestureDetected:
            gestureCounter += 1
            if gestureCounter > gestureDelay:
                gestureCounter = 0
                gestureDetected = False

        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    cv2.line(currImage, annotations[i][j - 1], annotations[i][j],(0,0,200),12)

        # adding webcam image on the slides
        imgSmall = cv2.resize(img, (pptCamWidth, pptCamHeight))
        h, w, _ = currImage.shape
        currImage[0:pptCamHeight, w-pptCamWidth:w] = imgSmall

        cv2.imshow("slides", currImage)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    


