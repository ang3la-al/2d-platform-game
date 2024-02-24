import pygame, sys 
from level import *
from HUD import *
from tiles import *
from transition import *

#controls level and transition creation
class Game:
    def __init__(self):
        self.max_level = 0  #initial max level
        
        self.max_health = 100
        self.current_health = 100
        self.gems = 0
        
        #sound
        self.level_track = pygame.mixer.Sound('Sound/Levels.wav')
        self.transition_track = pygame.mixer.Sound('Sound/Title Screen.wav')
        
        #creating transition state
        self.transition = Transition(0, self.max_level, screen, self.create_level)
        self.status = 'transition'  #intital status
        
        #looping music track
        self.transition_track.play(loops=-1)
        
        #HUD 
        self.HUD = HUD(screen)
        
    #creating new level
    def create_level(self,current_level):
        self.level = Level(current_level, screen, self.create_transition, self.gem_update, self.health_update)
        #when in level, game status = level
        self.status = 'level'
        
        #stop transition music, play level music
        self.transition_track.stop()
        self.level_track.play(loops=-1)
        
    #creating new transition
    def create_transition(self, current_level, new_max):
        if new_max > self.max_level:
            #updating max level
            self.max_level = new_max
        self.transition = Transition(current_level,self.max_level,screen,self.create_level)
        #updating to transition
        self.status = 'transition'
        self.level_track.stop()
        self.transition_track.play(loops=-1)


    def gem_update(self,amount):
        self.gems += amount
    
    def health_update(self,amount):
        self.current_health += amount

    def game_over(self):
        if self.current_health <=0:
            #resetting all attributes
            self.current_health = 100
            self.gems = 0
            self.max_level = 0
            self.transition = Transition(0, self.max_level, screen, self.create_level)
            self.status = 'transition'
            self.level_track.stop()
            self.transition_track.play(loops=-1)
    
    #run method
    def run(self):
        if self.status == 'transition':
            #run transition
            self.transition.run()
        else:
            #run level
            self.level.run()
            self.HUD.show_health(self.current_health,self.max_health)
            self.HUD.show_gems(self.gems)
            self.game_over()

#General setup, window dimensions
screen_height = 576
screen_width = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.init()

#setting FPS + loading bg image
clock = pygame.time.Clock()
bg_img = pygame.image.load('Images/Backgrounds/Forest/576.png')
game = Game()

#event handler, main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #run game class + drawing bg iamge
    screen.blit(bg_img,(0,0))
    game.run()
    
    #updating display
    pygame.display.update()
    clock.tick(60)