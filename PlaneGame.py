import pygame
from pygame.locals import *
import pygame.mixer
import random
from pygame.rect import Rect


# pygame setup
pygame.init()
Screen = pygame.display.set_mode((720, 850))
clock = pygame.time.Clock()
pygame.display.set_caption('Plane Game')
running = True
EnemyVisible = True  
GameOver = False

dt = 0  

ReplayButtonImage = pygame.image.load('Replay.png').convert_alpha()


def LaserSound(): 
    pygame.mixer.music.load("laser.wav")
    pygame.mixer.music.set_volume(0.05)  
    pygame.mixer.music.play()

def BombSound(): 
    pygame.mixer.music.load("bomb.wav")
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play()

def YouWinSound(): 
    pygame.mixer.music.load("YouWin.wav")
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play()

def GameOverSound(): 
    pygame.mixer.music.load("GameOver.wav")
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play()

def Background(): 
    background = pygame.image.load("background.jpg")
    Screen.blit(background,(0,0))

def YouWinText():
    Screen.blit(pygame.image.load('youwin.jpg'),((Screen.get_width() / 2) -300, (Screen.get_height() / 2 )-240))
    
def CheckWinCondition():
    return all(not visibility for visibility in enemy_visibility)

def IfGameOver():
    Screen.blit(pygame.image.load("bigExp.png"), ((plane.plane_position.x) - 350, (plane.plane_position.y) - 250))
    ReplayButtonSurface.update()
    Screen.blit(pygame.image.load("GameOver.jpg"),((plane.plane_position.x) - 265, (plane.plane_position.y) - 590))

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

#Enemies         
class Enemy(): 
    def __init__(self,coordinate1,coordinate2,hp=2): 
        self.hp = hp
        self.EnemyPos = pygame.Vector2(coordinate1,coordinate2)
        self.EnemyVelocityForX = 3
        self.EnemyVelocityForY =  1
        self.EnemyImage = pygame.image.load("enemies.png")
        
    def EnemyMove(self):
        self.EnemyPos.y += self.EnemyVelocityForY
        self.EnemyPos.x += self.EnemyVelocityForX
        
        #For X direction
        if self.EnemyPos.x <= -86 or  self.EnemyPos.x >= 566 :
            self.EnemyVelocityForX  *= -1
        
        #For Y direction
        if self.EnemyPos.y <= 0 or  self.EnemyPos.y >= 580 :
            
            dx = plane.plane_position.x - self.EnemyPos.x
            dy = plane.plane_position.y - self.EnemyPos.y
            distance = (dx**2 + dy**2)**0.5

            if distance != 0:
                dx /= distance
                dy /= distance

            # Adjust speed to make enemy follow the player
            speed = 7
            self.EnemyPos.x += dx * speed
            self.EnemyPos.y += dy * speed
        if EnemyVisible: 
            self.rect1 = Screen.blit(self.EnemyImage,(self.EnemyPos.x+52 ,self.EnemyPos.y-25))
        

class Bullet(): 
    def __init__(self): 
        self.PlaneBulletImage = pygame.image.load("bullet.png").convert() 
        self.BulletX = plane.plane_position.x 
        self.BulletY = plane.plane_position.y 
        self.BulletY_change = 10  

    def FireBullet(self,x,y): 
        self.BulletY -= self.BulletY_change
        self.rect2 = Screen.blit(self.PlaneBulletImage,(x+52 ,y-25))


class Plane():
    def __init__(self): 
        self.plane_position = pygame.Vector2(Screen.get_width() / 2 -50, Screen.get_height() / 2 + 300)
        self.plane = pygame.image.load("plane.png")


    def move(self):
        self.rect3 = Screen.blit(self.plane,self.plane_position)
        keys = pygame.key.get_pressed()
        #if keys[pygame.K_w] or keys[pygame.K_UP] and (self.plane_position.y >= +55 ):
        #    self.plane_position.y -= 450 * dt
        #if keys[pygame.K_s] or keys [pygame.K_DOWN] and (self.plane_position.y <= Screen.get_height()-105):
        #    self.plane_position.y += 450 * dt
        if keys[pygame.K_a] or keys [pygame.K_LEFT] and (self.plane_position.x > +4):
            self.plane_position.x -= 450 * dt    
        if keys[pygame.K_d] or keys [pygame.K_RIGHT] and (self.plane_position.x <Screen.get_width()-115):
            self.plane_position.x += 450 * dt

        #self.plane_position.x = min(max(self.plane_position.x, 0), 720 - Screen.get_width())
        #self.plane_position.y = min(max(self.plane_position.y, 0), 850 - Screen.get_height())

class Button(): 
    def __init__(self,image,x_pos,y_pos): 
        self.image = image  
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos,self.y_pos)) #creates a rect behind the button

    def update(self):
        Screen.blit(self.image,self.rect)

    def ReplayButtonCheck(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom): 
            restart_game() 


plane = Plane() 
bullets =[] 
enemy1 =Enemy((Screen.get_width() / 2), Screen.get_height() / 2 -260)
enemy2 =Enemy((Screen.get_width() / 2)+100, Screen.get_height() / 2 -370)
enemy3 =Enemy((Screen.get_width() / 2)-200, Screen.get_height() / 2 -270)
enemy4 =Enemy((Screen.get_width() / 2)-300, Screen.get_height() / 2 -370)
enemy5 =Enemy((Screen.get_width() / 2)-100, Screen.get_height() / 2 -170)

EnemiesList = [enemy1,enemy2,enemy3,enemy4,enemy5]

enemy_visibility = [True] * len(EnemiesList)
healthbar = HealthBar(100,20,100,20,100)

ReplayButtonSurface = pygame.transform.scale(ReplayButtonImage, (360, 550))
ReplayButtonSurface = Button(ReplayButtonImage, 360, 550)

def restart_game():
    global running, enemy_visibility, bullets, EnemiesList
    running = True
    enemy_visibility = [True] * len(EnemiesList)
    plane = Plane()
    bullets = []

    # Reset the positions of enemies
    EnemiesList = [
        Enemy((Screen.get_width() / 2), Screen.get_height() / 2 - 260),
        Enemy((Screen.get_width() / 2) + 100, Screen.get_height() / 2 - 370),
        Enemy((Screen.get_width() / 2) - 200, Screen.get_height() / 2 - 270),
        Enemy((Screen.get_width() / 2) - 300, Screen.get_height() / 2 - 370),
        Enemy((Screen.get_width() / 2) - 100, Screen.get_height() / 2 - 170)
    ]

while running:
    Background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE: 
            bullets.append(Bullet())  
            LaserSound()
        if event.type == pygame.MOUSEBUTTONDOWN:
            ReplayButtonSurface.ReplayButtonCheck(pygame.mouse.get_pos())
    # healthbar.hp = 50
    healthbar.Calculation()
    for bullet in bullets[:]:  
        bullet.FireBullet(bullet.BulletX, bullet.BulletY)
        for i, enemy in enumerate(EnemiesList): 
            if bullet.rect2.colliderect(enemy.rect1) and enemy_visibility[i]:
                if bullet in bullets: 
                    bullets.remove(bullet)
                enemy.hp -= 1
                # Update enemy visibility based on HP
                if enemy.hp <= 0:
                    enemy_visibility[i] = False
                    BombSound()
                    Screen.blit(pygame.image.load("explosion.png"),((enemy.EnemyPos.x)+25,(enemy.EnemyPos.y)-25))
    

    for i, enemy in enumerate(EnemiesList):
        if enemy_visibility[i]:
            enemy.EnemyMove()
            
              
    # fill the screen with a color to wipe away anything from last frame
    plane.move()

    for IndividualEnemy in EnemiesList:
        if (plane.plane_position.x-5) < IndividualEnemy.EnemyPos.x < (plane.plane_position.x+5) and (plane.plane_position.y-5) < IndividualEnemy.EnemyPos.y < (plane.plane_position.y+5):
            GameOver = True
            for i in range(len(EnemiesList)):
                enemy_visibility[i] = False
    
        
    if CheckWinCondition():
        YouWinText()
        ReplayButtonSurface.update()
    if GameOver: 
        IfGameOver()
        
            
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
pygame.quit()