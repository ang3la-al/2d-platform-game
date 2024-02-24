import pygame 
from tiles import *

class Ghost(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'Images/Enemies/Ghost/Idle')
        #setting speed to 1
        self.speed = 1
        
    #moves enemy horizontally
    def move(self):
        #updating x coordinates
        self.rect.x += self.speed
    
    #flips image when direction changes
    def reverse_image(self):
        #if moving right
        if self.speed > 0:
            #flip image
            self.image = pygame.transform.flip(self.image, True, False)
    
    #changes direction of enemy    
    def reverse(self):
        self.speed *= -1        
    
    #updates enemy
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        
class Fireskull(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'Images/Enemies/Fire Skull')
        self.speed = 0