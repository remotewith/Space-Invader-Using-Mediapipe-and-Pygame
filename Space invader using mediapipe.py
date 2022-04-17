import pygame

#initialize
pygame.init()

#create window/display
width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("DRAGONITE")

#initialize clock for fps
fps=30
clock=pygame.time.Clock()

#main loop
start=True
while start:
    
    #get events
    for event in pygame.event.get():#this function gets all the events frm pygame
        if event.type==pygame.QUIT:
            start=False
            pygame.quit()

    #Apply logic(main thing or content is written under this)
    window.fill((0,0,0))
    red,green,blue=(255,0,0),(0,255,0),(0,0,255)
    pygame.draw.polygon(window,green,((491,100),(788,100),(937,357),
                                       (788,614),(491,614),(342,357)))
    pygame.draw.circle(window,red,(640,360),200)
    pygame.draw.line(window,blue,(468,392),(812,392),4)
    pygame.draw.rect(window,blue,(468,307,345,70),border_radius=20)

    #Update Display
    pygame.display.update()

    #set FPS
    clock.tick(fps)