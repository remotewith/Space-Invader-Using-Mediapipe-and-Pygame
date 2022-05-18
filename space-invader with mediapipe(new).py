import pygame
import cv2
import numpy as np
import random
import thesius_module as the
import time

#"the" module
detector=the.handDetector(maxHands=1)


#initialize
pygame.init()

#create window/display
width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("DRAGONITE")

#Display shit
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)


#initialize clock for fps
fps=30
clock=pygame.time.Clock()

#Lives and Score
life=5
score=0

#Load Images
#imgBackground=pygame.image.load('background-black.png').convert()
imgEnemy=pygame.image.load("enemy.png").convert_alpha()
imgHero=pygame.image.load("spaceship.png").convert_alpha()
imgHero2=pygame.image.load("spaceship.png").convert_alpha()
shooter=pygame.image.load('pixel_laser_red.png').convert_alpha()

rectEnemy=imgEnemy.get_rect()#this function creates a rectangle around the desired image
rectHero=imgHero.get_rect()
rectHero2=imgHero2.get_rect()
rectLaser=shooter.get_rect()
rectHero.x,rectHero.y=-90,-90
rectHero2.x,rectHero2.y=-90,-90
rectLaser.x,rectLaser.y=-90,-90
rectEnemy.x,rectEnemy.y=500,0
#imgEnemy=pygame.transform.rotate(imgEnemy,90)
#imgEnemy=pygame.transform.flip(imgEnemy,False,True)


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#variables
speed=8
speedl=5

def resetEnemy():
    global speed
    rectEnemy.x=random.randint(100,img.shape[1]-100)
    rectEnemy.y=0
    speed+=.2

#main loop

start=True
lost=False

while start:

    t=0    #get events
    q=0    #for super move
    for event in pygame.event.get():#this function gets all the events frm pygame
        if event.type==pygame.QUIT:
            start=False
            pygame.quit()

    #Apply logic(main thing or content is written under this)
    
    _,img=cap.read()
    #img=cv2.flip(img,1)
    img=detector.findHands(img)
    
    lmList=detector.findPosition(img)

    rectEnemy.y=rectEnemy.y+speed

    if rectEnemy.y>height:
        life=life-1
        resetEnemy()
    

    
    if len(lmList)!=0:
        x,y=lmList[8][1],lmList[8][2]

        x=np.interp(x,[0,1240],[1280,0])
        x=int(x)
        y=np.interp(y,[0,720],[-20,640])
        y=int(y)
        rectHero.x=x
        rectHero.y=y

        
        
        if (lmList[8][2] > lmList[7][2]):
            if rectLaser.x==-90 and rectLaser.y==-90:
                rectLaser.x,rectLaser.y=(x-19),(y-57)
                rectLaser.x,rectLaser.y=(x-19),(y-57)
                x1,y1=rectLaser.x,rectLaser.y
                x1=np.interp(x1,[0,1240],[0,1280])
                x1=int(x1)
                y1=np.interp(y1,[0,720],[-20,640])
                y1=int(y1)
                rectLaser.x,rectLaser.y=x1,y1
                x1,y1=rectLaser.x,rectLaser.y

            else:
                rectLaser.y-=20
            t=1

        #print(rectEnemy.x,x)    #ERROR was HERE(NOW FIXED :)
        #print(rectEnemy.y,y)    #ERRROR was HERE(NOW FIXED :)
        
    
        if rectEnemy.collidepoint(x,y):
            score+=1
            resetEnemy()
        
        if t==1:
            
        
            if rectEnemy.collidepoint(rectLaser.x+60,rectLaser.y):

                score+=1
                resetEnemy()
    if score==20 and score!=30:
        if (lmList[8][2] > lmList[7][2] and lmList[12][2]>lmList[11][2]):
            x2,y2=lmList[12][1],lmList[12][2]
            rectHero2.x,rectHero2.y=x2,y2
            q=1
            
    #super_move(score)


    
    #Display
    text_surface = my_font.render("LIFE:"+str(int(life)), False, (0, 0, 0))
    text_surface1 = my_font.render("SCORE:"+str(int(score)), False, (0, 0, 0))


    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgRGB=np.rot90(imgRGB)
    frame=pygame.surfarray.make_surface(imgRGB).convert()
    window.blit(frame,(0,0))
    window.blit(imgEnemy,rectEnemy)
    window.blit(imgHero,rectHero)
    if t==1:
        window.blit(shooter,rectLaser)
    else:
        rectLaser.x,rectLaser.y=-90,-90
    if q==1:
        window.blit(imgHero2,rectHero2)
    else:
        rectHero2.x,rectHero2.y=-90,-90
    window.blit(text_surface, (30,30))
    window.blit(text_surface1, (1140,27))
    if score==17 and score!=0:
        text_surface2 = my_font.render("SPECIAL MOVE IS CLOSE", False, (0, 0, 0))
        text_surface3 = my_font.render(" USE YOUR OPEN PALM", False, (0, 0, 0))

        window.blit(text_surface2,(425,300))
        window.blit(text_surface3,(425,330))
    

    pygame.draw.rect(window, (0,255,0), pygame.Rect(30, 180, 25, 300),2)
    pygame.draw.rect(window,(0,255,0),pygame.Rect(30,180,25,((score%20)*15)))

    #Update Display
    pygame.display.update()

    #set FPS
    clock.tick(fps)