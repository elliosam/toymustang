import cv2 as cv
import numpy as np
import pickle

### PARKPERFORM: this code will display the video feed with an overlay of all the parking spots
### color coded to whether or not a car is there. meant to run in parallel with parkparse.py.

######## WRITTEN BY SAMUEL ELLIOTT 2024 ########

cap = cv.VideoCapture('assets/carPark.mp4')

with open('parkingPositions', 'rb') as f:
    shapes = pickle.load(f)

def updateColorFalse(img, shapeID):
    cv.line(img, (shapes[shapeID]['x1'], shapes[shapeID]['y1']), (shapes[shapeID]['x2'], shapes[shapeID]['y2']), (0,0,255), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x2'], shapes[shapeID]['y2']), (shapes[shapeID]['x3'], shapes[shapeID]['y3']), (0,0,255), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x3'], shapes[shapeID]['y3']), (shapes[shapeID]['x4'], shapes[shapeID]['y4']), (0,0,255), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x4'], shapes[shapeID]['y4']), (shapes[shapeID]['x1'], shapes[shapeID]['y1']), (0,0,255), 2, cv.LINE_AA)

def updateColorTrue(img, shapeID):
    cv.line(img, (shapes[shapeID]['x1'], shapes[shapeID]['y1']), (shapes[shapeID]['x2'], shapes[shapeID]['y2']), (0,255,0), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x2'], shapes[shapeID]['y2']), (shapes[shapeID]['x3'], shapes[shapeID]['y3']), (0,255,0), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x3'], shapes[shapeID]['y3']), (shapes[shapeID]['x4'], shapes[shapeID]['y4']), (0,255,0), 2, cv.LINE_AA)
    cv.line(img, (shapes[shapeID]['x4'], shapes[shapeID]['y4']), (shapes[shapeID]['x1'], shapes[shapeID]['y1']), (0,255,0), 2, cv.LINE_AA)

while(cap.isOpened()):
    ret, frame = cap.read()
    i = 0
    while i < len(shapes):
        if ret == True:
            if (shapes[i]['car'] == True):
                updateColorTrue(frame, i)
            else:
                updateColorFalse(frame, i)
            i += 1
        else:
            print("error getting frame, video may have ended")
            break