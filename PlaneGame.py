import pygame
from pygame.locals import *
import pygame.mixer


# pygame setup
pygame.init()
Screen = pygame.display.set_mode((720, 850))
clock = pygame.time.Clock()
pygame.display.set_caption('Plane Game')
running = True
dt = 0  


def LaserSound(): 
    pygame.mixer.music.load("laser.wav")
    pygame.mixer.music.set_volume(0.05)  
    pygame.mixer.music.play()

def Background(): 
    background = pygame.image.load("background.jpg")
    Screen.blit(background,(0,0))

class HealthBar(): 
    def __init__(self,x,y,w,h,max_hp): 
        self.HeartImage =  pygame.image.load("heart.png")
        self.x = x 
        self.y = y 
        self.w = w 
        self.h = h 
        self.hp = max_hp
        self.max_hp = max_hp
        
    
    def Calculation(self): 
        ratio = self.hp / self.max_hp
        Screen.blit(self.HeartImage,(self.x-55,self.y-6))
        pygame.draw.rect(Screen,"red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(Screen,"green",(self.x,self.y,self.w*ratio,self.h))
        

class Bullet(): 
    def __init__(self): 
        self.PlaneBulletImage = pygame.image.load("bullet.png").convert() 
        self.BulletX = plane.plane_position.x 
        self.BulletY = plane.plane_position.y 
        self.BulletY_change = 10  

    def FireBullet(self,x,y): 
        self.BulletY -= self.BulletY_change
        Screen.blit(self.PlaneBulletImage,(x+52 ,y-25))


class Plane():
    def __init__(self): 
        self.plane_position = pygame.Vector2(Screen.get_width() / 2 -50, Screen.get_height() / 2 + 300)
        self.plane = pygame.image.load("plane.png")


    def move(self):
        Screen.blit(self.plane,self.plane_position)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP] and (self.plane_position.y >= +55 ):
            self.plane_position.y -= 450 * dt
        if keys[pygame.K_s] or keys [pygame.K_DOWN] and (self.plane_position.y <= Screen.get_height()-105):
            self.plane_position.y += 450 * dt
        if keys[pygame.K_a] or keys [pygame.K_LEFT] and (self.plane_position.x > +4):
            self.plane_position.x -= 450 * dt    
        if keys[pygame.K_d] or keys [pygame.K_RIGHT] and (self.plane_position.x <Screen.get_width()-115):
            self.plane_position.x += 450 * dt

        #self.plane_position.x = min(max(self.plane_position.x, 0), 720 - Screen.get_width())
        #self.plane_position.y = min(max(self.plane_position.y, 0), 850 - Screen.get_height())


plane = Plane() 
bullets =[] 

healthbar = HealthBar(100,20,100,20,100)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE: 
            bullets.append(Bullet()) 
            LaserSound()
    Background()
    # healthbar.hp = 50
    healthbar.Calculation()
    for bullet in bullets: 
        bullet.FireBullet(bullet.BulletX,bullet.BulletY)

        if bullet.BulletY < 70 :
            bullets.remove(bullet)
                
    # fill the screen with a color to wipe away anything from last frame
    plane.move()
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
pygame.quit()