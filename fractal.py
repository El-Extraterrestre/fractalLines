import pygame
from random import randint
from time import sleep
from math import sin, cos, pi

deg2rad = pi/180

pygame.init()

#width,hight = int(1920/2), int(1080/2)
width,hight = 1920, 1080
screen = pygame.display.set_mode((width,hight))

#helper for RGB calculation
def farbGraph(inX):
    x = inX % 360
    if x <60:
        return int((x * 255) / 60)
    elif x < 180:
        return 255
    elif x < 240:
        return int((255 - ((x - 180) * 255) / 60))
    elif x < 360:
        return 0
    else:
        return -1

#Hue to RGB Conversion
def HtoRGB(h):
    return (farbGraph(h+240),farbGraph(h),farbGraph(h+120))

#from Points Tuple to vector
#y1-x1,y2-x2
def toVector(points):
    return (points[1][0]-points[0][0],points[1][1]-points[0][1])


def pointPlusVector(p,v):
    return (p[0]+v[0],p[1]+v[1])

#change the length of a vector
def vectorLengthPercent(v,p):
    return (v[0]*p,v[1]*p)

def vectorRotate(v,a):
    rad = a * deg2rad
    ca = cos(rad)
    sa = sin(rad)
    return (round(ca*v[0]-sa*v[1],4),round(sa*v[0]+ca*v[1],4))

#draws lines to the screen uses color based on line number in the array
#updates the screen for grow effect
def drawLines(scr, arr):
    l = len(arr)
    i = 0
    for a in arr:
        pygame.draw.line(scr, HtoRGB(i*360/l), a[0],a[1])
        pygame.display.flip()
        i += 1


#different fractal function. takes an array of lines
#and duplicates lines based on an rule set
  
#   /
#   -
#   /
def fract1(inAr):
    tempAr = []
    for point in inAr:
        pA = point[0]
        pX = pointPlusVector(pA,vectorLengthPercent(toVector(point),0.5))
        pB = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.25),90))
        pC = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.25),270))
        pD = point[1]
        tempAr.append((pA,pB))
        tempAr.append((pB,pC))
        tempAr.append((pC,pD))
    return tempAr

#  |
#--|
#  |
def fract2(inAr):
    tempAr = []
    for point in inAr:
        pA = point[0]
        pX = pointPlusVector(pA,vectorLengthPercent(toVector(point),0.5))
        pB = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.5),90))
        pC = point[1]
        tempAr.append((pA,pB))
        tempAr.append((pB,pC))
    return tempAr

#-
# |
#-
def fract3(inAr):
    tempAr = []
    for point in inAr:
        pA = point[0]
        pX = pointPlusVector(pA,vectorLengthPercent(toVector(point),0.5))
        pB = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.5),90))
        pC = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.5),270))
        pD = point[1]
        tempAr.append((pA,pX))
        tempAr.append((pB,pX))
        #tempAr.append((pC,pX))
        tempAr.append((pX,pD))
    return tempAr

# /
# /
def fract4(inAr):
    tempAr = []
    for point in inAr:
        v = vectorLengthPercent(toVector(point),0.25)
        pA = pointPlusVector(point[0],vectorRotate(v,90))
        pB = pointPlusVector(point[0],vectorLengthPercent(toVector(point),0.5))
        pC = pointPlusVector(point[1],vectorRotate(v,270))
        tempAr.append((pA,pB))
        tempAr.append((pB,pC))
    return tempAr

#\
#/
def fract5(inAr):
    tempAr = []
    for point in inAr:
        pA = point[0]
        pX = pointPlusVector(pA,vectorLengthPercent(toVector(point),0.5))
        pB = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.5),300))
        pD = point[1]
        tempAr.append((pA,pB))
        tempAr.append((pB,pD))
    return tempAr

#-
#/
def fract6(inAr):
    tempAr = []
    for point in inAr:
        pA = point[0]
        pX = pointPlusVector(pA,vectorLengthPercent(toVector(point),0.25))
        pB = pointPlusVector(pX,vectorRotate(vectorLengthPercent(toVector(point),0.25),30))
        pD = point[1]
        tempAr.append((pA,pB))
        tempAr.append((pB,pD))
    return tempAr

#generates new starting position
#based 
#param -array   int fractal
#               int recursion steps
#               bool smaller starting point
def drawFract(data):
    startPoint = (randint(int(width/4),int(width-width/4)), randint(int(hight/8),int(hight/8+hight/16))), (randint(int(width/4),int(width-width/4)),randint(int(hight-hight/8),int(hight-hight/8+hight/16)))
    fract = [fract1, fract2, fract3, fract4, fract5, fract6]
    if data[2]:
        startPoint = (randint(int(width/4),int(width-width/4)), randint(int(hight/4),int(hight/4+hight/16))), (randint(int(width/4),int(width-width/4)),randint(int(hight-hight/2),int(hight-hight/2+hight/16)))

    
    screen.fill((0,0,0))
    myLines = []
    myLines.append(startPoint)
    drawLines(screen, myLines)
    for i in range(data[1]):
        sleep(0.5)
        screen.fill((0,0,0))
        myLines = fract[data[0]](myLines)
        drawLines(screen,myLines)

#predefined value for diffrent fractals
allFracts = [[1,8,True],[3,10,False],[2,7,False],[5,9,False],[0,7,False],[4,8,True]]


#main loop
#event Handler to close the Window
#randomly chooses a fractal function with its presets
while(True):
    x = randint(0,5)
    drawFract(allFracts[x])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            
    pygame.display.flip()
    sleep(0.5)
