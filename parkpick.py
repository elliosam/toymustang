import cv2 as cv
import numpy as np
import pickle
xpoints = []
ypoints = []
a=0
try:
    with open('parkingPositions', 'rb') as f:
        shapes = pickle.load(f)
except:
    shapes = []
    
def eq1(xs, x1, y1, x2, y2, yint1):
    sol1=yint1 + (((y2-y1)/(x2-x1))*xs)
    return sol1

def eq2(xs, xo, yo, x1, y1, x2, y2):
    sol2=yint2(xo, yo, x1, y1, x2, y2) + (((y2-y1)/(x2-x1))*xs)
    return sol2

def yint2(xo,yo,x1,y1,x2,y2):
    int2=(y1-yo)+(((y1-y2)/(x1-x2))*(x1-xo))
    return int2

def findyx(xin,b1x,b1y,a2x,a2y,b2x,b2y,a1y):
    if (xin==b1x):
        yx=b1y
    elif (xin==a2x):
        yx=a2y
    elif (xin==b2x):
        yx=b2y
    else:
        yx=a1y
    return yx


def mouseClick(events,x,y,flags,params):
    if events ==cv.EVENT_LBUTTONDOWN:
        xpoints.append(x)
        ypoints.append(y)
        print(xpoints)
        print(ypoints)
    # only code I added you have to hit button twice but its a lot easier than having to manually type in the terminal
        if len(xpoints) == 4:#4 dots
            keycode=cv.waitKeyEx(0)
            print(keycode)
            if keycode==121:
                TruFals=True
            if keycode==110:
                TruFals=False
    #end
            else:
                print('lmao how did you do that')
                a=0
            shapes.append({
                "x1": xpoints[0],
                "y1": ypoints[0],
                "x2": xpoints[1],
                "y2": ypoints[1],
                "x3": xpoints[2],
                "y3": ypoints[2],
                "x4": xpoints[3],
                "y4": ypoints[3],
                "car": TruFals
            })
            print('Is car? Y/N')
            keycode=cv.waitKeyEx(0)
            print(shapes)
            
            # reset the pointCount to start over
            xpoints.clear()
            ypoints.clear()
        cv.imshow('dots', bg)
    elif events ==cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(shapes):
            xlist=[pos['x1'],pos['x2'],pos['x3'],pos['x4']]
            xlist.sort()
            ylist=[pos['y1'],pos['y2'],pos['y3'],pos['y4']]
            ylist.sort()
            ylo=ylist[0]
            yhi=ylist[3]
            xlo,xm1,xm2,xhi=xlist
            yxlo=findyx(xlo,pos['x1'],pos['y1'],pos['x2'],pos['y2'],pos['x3'],pos['y3'],pos['y4'])
            yxm1=findyx(xm1,pos['x1'],pos['y1'],pos['x2'],pos['y2'],pos['x3'],pos['y3'],pos['y4'])
            yxm2=findyx(xm2,pos['x1'],pos['y1'],pos['x2'],pos['y2'],pos['x3'],pos['y3'],pos['y4'])
            yxhi=findyx(xhi,pos['x1'],pos['y1'],pos['x2'],pos['y2'],pos['x3'],pos['y3'],pos['y4'])
            if yxm1>yxm2:
                xmhi=xm1
                yxmhi=yxm1
                xmlo=xm2
                yxmlo=yxm2
            else:
                xmhi=xm2
                yxmhi=yxm2
                xmlo=xm1
                yxmlo=yxm1
            xs=x - xlo
            ys=y - ylo
            yint1=yxlo-ylo
            if ((xlo<x<xhi)&(ylo<y<yhi)):
                if ((((xs <= xmhi)&(ys < eq1(xs, xlo, yxlo, xmhi, yxmhi, yint1)))|
                    ((xs > xmhi)&(ys < eq2(xs, xlo, ylo, xmhi, yxmhi, xhi, yxhi))))&
                    (((xs <= xmlo)&(ys > eq1(xs, xlo, yxlo, xmlo, yxmlo, yint1)))|
                    ((xs > xmlo)&(ys > eq2(xs, xlo, ylo, xmlo, yxmlo, xhi, yxhi))))):
                    shapes.pop(i)
                    print("Box Cleared")
    elif events == cv.EVENT_RBUTTONDBLCLK:
        print("CLEARING")
        cv.imshow('dots', bg)
        shapes.clear()
        xpoints.clear()
        ypoints.clear()
    
    with open('parkingPositions', 'wb') as f:
        pickle.dump(shapes, f)


shapes.clear() #Uncomment this; start up code; then comment it again to clear shapes
while True:
    # orig=cv.imread('assets/parkingLotAerial.png')
    # bg=cv.resize(orig,(1280,720), interpolation=cv.INTER_CUBIC)
    
    bg=cv.imread('assets/parkingLotAerial.png')
    
    cv.imshow('dots',bg)
    if len(xpoints) >= 1:
        cv.circle(bg, (xpoints[0],ypoints[0]), 2, (0,0,255), 2, cv.FILLED)
    if len(xpoints) >= 2:#2 dots
        cv.circle(bg, (xpoints[1],ypoints[1]), 2, (0,0,255), 2, cv.FILLED)
        cv.line(bg, (xpoints[0], ypoints[0]), (xpoints[1], ypoints[1]), (255,0,0), 2, cv.LINE_AA)            
    if len(xpoints) >= 3:#3 dots
        cv.circle(bg, (xpoints[2],ypoints[2]), 2, (0,0,255), 2, cv.FILLED)
        cv.line(bg, (xpoints[1], ypoints[1]), (xpoints[2], ypoints[2]), (255,0,0), 2, cv.LINE_AA)
       
    for pos in shapes:    
        cv.line(bg, (pos['x1'], pos['y1']), (pos['x2'], pos['y2']), (255,0,0), 2, cv.LINE_AA)
        cv.line(bg, (pos['x2'], pos['y2']), (pos['x3'], pos['y3']), (255,0,0), 2, cv.LINE_AA)
        cv.line(bg, (pos['x3'], pos['y3']), (pos['x4'], pos['y4']), (255,0,0), 2, cv.LINE_AA)
        cv.line(bg, (pos['x4'], pos['y4']), (pos['x1'], pos['y1']), (255,0,0), 2, cv.LINE_AA)
    cv.imshow('dots',bg)    
    cv.setMouseCallback('dots',mouseClick)
    if cv.waitKey(1) & 0xFF == ord('q'):#Press q to exit program
        break