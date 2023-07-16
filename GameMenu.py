import pygame
import pygame.mixer

#game window
pygame.init() 

clock = pygame.time.Clock()

#set screen display
Screen = pygame.display.set_mode((720, 850))

#set caption
pygame.display.set_caption('Plane Game Menu')

#used for while loop
running = True 

#background image
BackgroundImage = pygame.image.load("background.jpg") # gokalp not: her frame yuklememek icin disari aldim 

#first menu images (Buttons and Text)
StartButtonImage = pygame.image.load("start_btn.png").convert_alpha()
ExitButtonImage = pygame.image.load("exit_btn.png").convert_alpha()
ArdaTextImage = pygame.image.load("ardac.png").convert_alpha()
MuteButtonImage = pygame.image.load("mute_button.png").convert_alpha()

#menu music
pygame.mixer.music.load("HighNoon_TrackTribe.mp3")
pygame.mixer.music.set_volume(0.2)

#new icon 
NewIcon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(NewIcon)

def Background(): 
    Screen.blit(BackgroundImage,(0,0))

def PlayMusic(): 
    pygame.mixer.music.play()

def PauseMusic(): 
    pygame.mixer.music.pause()

def ArdaText(): 
    Screen.blit(ArdaTextImage,(210,550))
     
class Button(): 
    def __init__(self,image,x_pos,y_pos): 
        self.image = image  
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos,self.y_pos)) #creates a rect behind the button

    def update(self):
        Screen.blit(self.image,self.rect)

    def StartButtonCheck(self,position):
        if position[0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top,self.rect.bottom): 
            print("Start Pressed") 

    def ExitButtonCheck(self,position): 
        if position[0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top,self.rect.bottom): 
            pygame.quit()
            
    def MuteButtonCheck(self,position):
        if position[0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top,self.rect.bottom): 
            PauseMusic()
             
    
        
#screen.blit(start_img,(screen.get_width()/2-150,(screen.get_height()/2) -170))
#screen.blit(exit_img,(screen.get_width()/2 -127.5,(screen.get_height()/2) +10 ))
#screen.blit(mute_img,(screen.get_width() -90 ,(screen.get_height()/2) -400 ))

#start button
StartButtonSurface = pygame.transform.scale(StartButtonImage, (360, 250))
StartButtonSurface = Button(StartButtonImage, 360, 250)

ExitButtonSurface = pygame.transform.scale(ExitButtonImage, (362, 430))
ExitButtonSurface = Button(ExitButtonImage, 362, 430)

MuteButtonSurface = pygame.transform.scale(MuteButtonImage, (650, 65))
MuteButtonSurface = Button(MuteButtonImage, 650, 65)


PlayMusic()

while running:  
    Background()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            StartButtonSurface.StartButtonCheck(pygame.mouse.get_pos())
            ExitButtonSurface.ExitButtonCheck(pygame.mouse.get_pos())
            MuteButtonSurface.MuteButtonCheck(pygame.mouse.get_pos())
    
    StartButtonSurface.update()
    ExitButtonSurface.update()
    MuteButtonSurface.update()
    ArdaText()
    pygame.display.update()
    clock.tick(60)
pygame.quit()