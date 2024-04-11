import cv2 as cv
import numpy as np
import pickle
import pandas as pd

orig = cv.imread('assets/parkingLotAerial.png')
im=cv.resize(orig,(1280,720), interpolation=cv.INTER_CUBIC)

img33 = np.zeros((im.shape[0], im.shape[1], 3), dtype = np.uint8)
#originally had this using blured image didnt want to chanmge the name in the rest of the code
blurred = im
j=0
data=pd.read_csv('varhogdata')
print(data)
i=0
shapes=[]
print(data['x1'].loc[data.index[1]])
while i<69:
    shapes.append({
                "x1": data['x1'].loc[data.index[i]],
                "y1": data['y1'].loc[data.index[i]],
                "x2": data['x2'].loc[data.index[i]],
                "y2": data['y2'].loc[data.index[i]],
                "x3": data['x3'].loc[data.index[i]],
                "y3": data['y3'].loc[data.index[i]],
                "x4": data['x4'].loc[data.index[i]],
                "y4": data['y4'].loc[data.index[i]],
                "car": data['car'].loc[data.index[i]],
                
                
            })
    cv.circle(blurred, ((shapes[i]['x1'],shapes[i]['y1'])), 2, (0,0,255), 2, cv.FILLED)
    cv.circle(blurred, ((shapes[i]['x2'],shapes[i]['y2'])), 2, (0,0,255), 2, cv.FILLED)
    cv.circle(blurred, ((shapes[i]['x3'],shapes[i]['y3'])), 2, (0,0,255), 2, cv.FILLED)
    cv.circle(blurred, ((shapes[i]['x4'],shapes[i]['y4'])), 2, (0,0,255), 2, cv.FILLED)
    ymax=np.array(max(shapes[i]['y1'],shapes[i]['y2'],shapes[i]['y3'],shapes[i]['y4']))
    ymin=np.array(min(shapes[i]['y1'],shapes[i]['y2'],shapes[i]['y3'],shapes[i]['y4']))
    xmax=np.array(max(shapes[i]['x1'],shapes[i]['x2'],shapes[i]['x3'],shapes[i]['x4']))
    xmin=np.array(min(shapes[i]['x1'],shapes[i]['x2'],shapes[i]['x3'],shapes[i]['x4']))
    
    xmid=(xmax+xmin-20)/2
    ymid=(ymax+ymin)/2
    points=int(xmid),int(ymid)
    counter=str(len(shapes)-1)
    cv.putText(blurred,counter,(points),cv.FONT_HERSHEY_SIMPLEX, .4,(0,0,0), 2,2)
    cv.putText(blurred,counter,(points),cv.FONT_HERSHEY_SIMPLEX, .4,(255,255,255), 1,2)
   
    if shapes[i]['car']==True:
        cv.line(blurred,(shapes[i]['x1'],shapes[i]['y1']),(shapes[i]['x2'],shapes[i]['y2']), (0, 255, 0), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x2'],shapes[i]['y2']),(shapes[i]['x3'],shapes[i]['y3']), (0, 255, 0), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x3'],shapes[i]['y3']),(shapes[i]['x4'],shapes[i]['y4']), (0, 255, 0), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x4'],shapes[i]['y4']),(shapes[i]['x1'],shapes[i]['y1']), (0, 255, 0), 2, cv.LINE_AA)
    else:
        cv.line(blurred,(shapes[i]['x1'],shapes[i]['y1']),(shapes[i]['x2'],shapes[i]['y2']), (0, 0, 255), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x2'],shapes[i]['y2']),(shapes[i]['x3'],shapes[i]['y3']), (0, 0, 255), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x3'],shapes[i]['y3']),(shapes[i]['x4'],shapes[i]['y4']), (0, 0, 255), 2, cv.LINE_AA)
        cv.line(blurred,(shapes[i]['x4'],shapes[i]['y4']),(shapes[i]['x1'],shapes[i]['y1']), (0, 0, 255), 2, cv.LINE_AA)
    i+=1
with open('parkingPositions', 'wb') as f:
        pickle.dump(shapes, f)
    
   

print(shapes)
cv.imshow('Filter',blurred)
cv.waitKey(0)