import pygame
from os import walk
from math import sin

def import_folder(path):
    for _,__,image_files in walk(path):
        surface_list = []
        for image in image_files:
            #adding image name to path, getting full file path
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            #adding images to surface_list
            surface_list.append(image_surf)
        return surface_list
    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, health_update):
        super().__init__()
        #player images
        self.import_img()  #importing images from support
        self.animation_frame = 0   
        self.animation_speed = 0.15 #setting animation frame speed
        self.image = self.animations['Idle'][self.animation_frame]
        self.rect = self.image.get_rect(topleft = pos)
        
        #player movement variables
        self.direction = pygame.math.Vector2(0,0)   
        self.speed = 6
        self.gravity = 0.5
        self.jump_speed = -10

        #player status
        self.status = 'Idle'
        #default player states
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        #HUD - health attributes
        self.health_update = health_update
        self.immune = False
        self.immunity_cooldown = 450
        self.time_damaged = 0
        
        #player sounds
        self.jumping_sound = pygame.mixer.Sound('Sound/Jumping.wav')
        self.damaged_sound = pygame.mixer.Sound('Sound/Damaged.wav')
        

    def import_img(self):
        #animations stored
        player_directory = 'Images/Player/'
        #defining dictionary and empty lists
        self.animations = {'Idle':[],'Run':[],'Death':[],'Jump':[]}
        
        #looping through each animation, loading images
        for animation in self.animations.keys():
            #full path of animation
            full_path = player_directory + animation
            #loading images into a folder, adding to list
            self.animations[animation] = import_folder(full_path)
            
    def animate(self):
        #assigning animation based on status
        animation = self.animations[self.status]
        
        #add animation speed to frame index
        self.animation_frame += self.animation_speed
        #looping through animation
        if self.animation_frame >= len(animation):
            self.animation_frame = 0
        #get current image
        image = animation[int(self.animation_frame)]
        #flip image if player is facing left
        if self.facing_right:
            self.image = image
        else:   #Flipping image on x axis
            self.image = pygame.transform.flip(image,True, False)
            
        if self.immune:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
        #setting rect border/updating pos for all collision scenarios
        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            elif self.on_left:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(topright = self.rect.topright)
            elif self.on_left:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
            else:
                self.rect = self.image.get_rect(midtop = self.rect.midtop)

    #setting keyboard presses for player movement        
    def user_input(self):
        #if right arrow pressed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            #set x direction to right
            self.direction.x = 1
            #player faces right
            self.facing_right = True
        #if left arrow pressed
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            #set x direction to left
            self.direction.x = -1
            #facing left
            self.facing_right = False 
        else:
            #if nothing pressed, stop movement
            self.direction.x = 0
        #jump only when on ground
        if pygame.key.get_pressed()[pygame.K_UP] and self.on_ground:
            self.jump() 
    
    #calculating player status, e.g: Idle, Run            
    def get_status(self):
        #check player direction
        if self.direction.y < 0:
            #moving up = jump
            self.status = 'Jump'
        elif self.direction.x != 0:
            #moving left/right = run
            self.status = 'Run'
        else:
            #no movement = idle
            self.status = 'Idle'

    def apply_gravity(self):
        #apply gravity if above the ground
        self.direction.y += self.gravity
        #update y coordinates
        self.rect.y += self.direction.y        
        
    def jump(self):
        #change direction to jump
        self.direction.y = self.jump_speed    
        self.jumping_sound.play()
        
    def calculate_damage(self):
        #if player not immune
        if not self.immune:
            self.damaged_sound.play()
            #update health
            self.health_update(-20)
            #set to immune
            self.immune = True
            self.time_damaged = pygame.time.get_ticks()
            
    def immunity_timer(self):
        #If immune
        if self.immune:
            #check cooldown time elapsed
            if pygame.time.get_ticks() - self.time_damaged >= self.immunity_cooldown:
                #set to false
                self.immune = False
    
    #to give flinching effect            
    def wave_value(self):
        #making a sin wave
        val = sin(pygame.time.get_ticks())
        if val >= 0: 
            return 255  #transparency
        else: 
            return 0 
            
    #updating player
    def update(self):
        self.user_input()
        self.get_status()
        self.animate()
        self.immunity_timer()
        self.wave_value()