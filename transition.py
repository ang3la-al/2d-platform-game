import pygame

#defining level attributes
level1 = {'position':(500,225), 'content': 'this is level 1', 'unlock':1}
level2 = {'position':(500,300), 'content': 'this is level 2', 'unlock':2}
level3 = {'position':(500,375), 'content': 'this is level 3', 'unlock':3}

#creating a dictionary
levels = {
    0: level1,
    1: level2,
    2: level3}

#class for choices
class Choice(pygame.sprite.Sprite):
    def __init__(self, pos, status, avatar_speed, level):
        super().__init__()

        #what image should load, depending on level
        if level == 1:
            self.image = pygame.image.load('Images/Transition/0.png').convert_alpha()
        elif level == 2:
            self.image = pygame.image.load('Images/Transition/1.png').convert_alpha()
        elif level == 3:
            self.image = pygame.image.load('Images/Transition/2.png').convert_alpha()    
        #updating choice status
        if status == 'unlocked':
            self.status = 'unlocked'
        else:
            self.status = 'locked'
            
        #set the position of the sprite
        self.rect = self.image.get_rect(center = pos)
        #defining collision border
        self.collision_border = pygame.Rect(self.rect.centerx-(avatar_speed/2),self.rect.centery-(avatar_speed/2),avatar_speed,avatar_speed)

#class for avatar sprite        
class Avatar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #setting position of avatar
        self.pos = pos
        #loading key image
        self.image = pygame.image.load('Images/Transition/key.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        #updating center position for collisions
        self.rect.center = self.pos
        
class Transition:
    def __init__(self, start_level, max_level, surface, create_level):
        #general setup of game state variables
        self.display_surface = surface 
        #highest level unlocked by player
        self.max_level = max_level 
        #players current level
        self.current_level = start_level   
        #creating next level
        self.create_level = create_level   
        
        #movement attributes
        self.moving = False
        #player movement direction
        self.move_direction = pygame.math.Vector2(0,0)  
        self.speed = 5
        
        #setup for choice and avatar
        self.choice_setup()
        self.avatar_setup()
        
    #defining button positions
    def choice_setup(self):
        #sprite group
        self.choices = pygame.sprite.Group()
        #looping through levels to create a button
        for index, position in enumerate(levels.values()):
            #if level unlocked, create unlocked button
            if index <= self.max_level:
                choice_sprite = Choice(position['position'],'unlocked', self.speed, index+1)
            else:
                #if level locked, create locked button
                choice_sprite = Choice(position['position'],'locked', self.speed, index+1)
            #add the button to the sprite group
            self.choices.add(choice_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            #positioning choice for levels up to max level
            points = [choice['position'] for index, choice in enumerate(levels.values())if index <= self.max_level]
            #draw lines connecting choices
            pygame.draw.lines(self.display_surface,'white', False, points, 6)
    
    def avatar_setup(self):
        #creating sprite group for avatar
        self.avatar = pygame.sprite.GroupSingle()
        #position at current level, creating new sprite at position
        avatar_sprite = Avatar(self.choices.sprites()[self.current_level].rect.center)
        #adding to sprite group
        self.avatar.add(avatar_sprite)
    
    def input(self):
        #check if currently moving
        if not self.moving:
            #if pressed and more levels unlocked downwards
            if pygame.key.get_pressed()[pygame.K_DOWN] and self.current_level < self.max_level:
                #set movement direction
                self.move_direction = self.get_movement('next')
                #increment level
                self.current_level += 1
                self.moving = True
            #if pressed and more levels unlocked upwards
            elif pygame.key.get_pressed()[pygame.K_UP] and self.current_level > 0:
                #set movement direction
                self.move_direction = self.get_movement('previous')
                #decrement level
                self.current_level -= 1
                self.moving = True
            #when space is pressed create/load level
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                self.create_level(self.current_level)
                
    def update_avatar(self):
        #check if moving + which direction
        if self.moving and self.move_direction:
            #updating sprite position
            self.avatar.sprite.pos += self.move_direction * self.speed
            #destination choice sprite for current level
            destination_choice = self.choices.sprites()[self.current_level]
            #check collision with border
            if destination_choice.collision_border.collidepoint(self.avatar.sprite.pos):
                #reset movement variables
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
    
    def get_movement(self, destination):
        #get center for current level
        start = pygame.math.Vector2(self.choices.sprites()[self.current_level].rect.center)
        #center point of destination depending on the destination parameter
        if destination == 'next':
            end = pygame.math.Vector2(self.choices.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.choices.sprites()[self.current_level - 1].rect.center)
        #return normalized vector, start to end point
        return (end-start).normalize()
            
    def run(self):
        #player input
        self.input()
        #updating avatar sprite movement
        self.update_avatar()
        self.avatar.update()
        #draw paths to screen
        self.draw_paths()   
        #draw choices to screen
        self.choices.draw(self.display_surface)
        #draw avatar to screen
        self.avatar.draw(self.display_surface)