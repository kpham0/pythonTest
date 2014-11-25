import pygame, sys, random
from pygame.locals import *
pygame.init()

class Truck(pygame.sprite.Sprite):
    animation = []
    fps = 0
    numframes = 0
    currentframe = 0
    lastdisplay = 0
    xspeed = 0
    yspeed = 0
    
    def __init__(self, anim, fps, currentx, currenty): 
        pygame.sprite.Sprite.__init__(self)
        
        self.animation = anim 
        self.numframes = len(anim)
        self.fps = fps
        self.image = anim[0]
        self.rect = anim[0].get_rect()
        self.rect.centerx = currentx
        self.rect.centery = currenty
            
    def update(self, secs):
        ############### animation #################
        self.image = self.animation[self.currentframe]
        self.lastdisplay = self.lastdisplay+secs
        if self.lastdisplay > self.fps:
            self.lastdisplay = 0
            self.currentframe = self.currentframe+1
            if self.currentframe == self.numframes:
                self.currentframe = 0
                
        ############# movement #####################
        self.rect.centerx = self.rect.centerx + self.xspeed
        self.rect.centery = self.rect.centery + self.yspeed
        
    def setXSpeed(self, xval):
        self.xspeed = xval
        
    def setYSpeed(self, yval):
        self.yspeed = yval
        
    def setAnimation(self, anim, fps):
        self.animation = anim 
        
class Rock(pygame.sprite.Sprite):
    health = 10
    
    def __init__(self, filename, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.image.load(filename).convert()
        img.set_colorkey((255,255,255))
        self.image = img 
        self.rect = img.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        

def makeAnimation(filename, numframes, transkey=False):
    animg = pygame.image.load(filename).convert()
    if transkey != False:
        animg.set_colorkey(transkey)
        
    w = animg.get_rect().w
    h = animg.get_rect().h
    
    imgw = w/numframes
    imgh = h 
    cframe = 0
    cx = 0
    cy = 0
    framelist = []
    
    while cframe < numframes:
        timg = animg.subsurface(cx,cy,imgw,imgh)
        framelist.append(timg)
        cx = cx + imgw
        cframe = cframe+1
        
    return framelist

def makeSetup(backgroundname):
    clock = pygame.time.Clock()
    background = pygame.image.load(backgroundname)
    w = background.get_rect().w
    h = background.get_rect().h
    
    screen = pygame.display.set_mode((w,h))
    
    return clock, background, screen

################## main game code #########################
clock, backg, screen = makeSetup("woods.jpg")
displayGroup = pygame.sprite.Group()
collgroup = pygame.sprite.Group()

truckleftarray = makeAnimation("truckleft.png", 9, (255,165,181)) 
truckrightarray = makeAnimation("truckright.png", 9, (255,165,181))

fps = .05

sptruckleft = Truck(truckleftarray,fps,50,50)
sptruckright = Truck(truckrightarray,fps,150,120)
rock1 = Rock("rock.png", 450,200)
rock2 = Rock("rock.png", 300,300)

displayGroup.add(rock1)
displayGroup.add(rock2)
displayGroup.add(sptruckleft)
displayGroup.add(sptruckright)
collgroup.add(rock1)
collgroup.add(rock2)



screen.blit(backg,(0,0))
moveflag = False

while True:
    secs = clock.tick(30)/1000
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT: sys.exit()
        
        if event.type==pygame.KEYUP:
            moveflag = False
            sptruckright.setXSpeed(0)
            sptruckright.setYSpeed(0)
        
        if event.type==pygame.KEYDOWN:
            moveflag = True
            if event.key == pygame.K_RIGHT: 
                sptruckright.setXSpeed(5)
                sptruckright.setAnimation(truckrightarray, fps)
            if event.key == pygame.K_LEFT: 
                sptruckright.setXSpeed(-5)
                sptruckright.setAnimation(truckleftarray,fps)
                
            if event.key == pygame.K_UP: sptruckright.setYSpeed(-5)
            if event.key==pygame.K_DOWN: sptruckright.setYSpeed(5)
            
    collist = pygame.sprite.spritecollide(sptruckright, collgroup, False)
    
    if len(collist)>0:
        spx = collist[0]
        spx.health = spx.health-3
        if spx.health <= 0:
            displayGroup.remove(spx)
        displayGroup.remove(sptruckright)
        
            
    
        
    displayGroup.clear(screen,backg)
    displayGroup.update(secs)
    displayGroup.draw(screen)
    
    pygame.display.flip()
