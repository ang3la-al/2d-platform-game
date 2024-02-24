import pygame
from os import walk

def load_sprites(path):
    #empty list for surface
    surface_list = []
    #to work through file directory
    for _,__,image_files in walk(path):
        #for each path, loop over files
        for image in image_files:
            #work out full path
            full_path = path + '/' + image
            #load and convert image to surface
            image_surface = pygame.image.load(full_path).convert_alpha()
            #add surface to list
            surface_list.append(image_surface)
    #retrun list of surfaces
    return surface_list

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def update(self, shift):
        self.rect.x += shift

#multiple stationary tiles        
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

#single terrain for gems        
class Gems(StaticTile):        
    def __init__(self, size, x, y, path, value):
        super().__init__(size,x,y,path)
        self.value = value

#adds animation functionality to Tile
class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        #loading animation images
        self.frames = load_sprites(path)
        #setting first image to first animation frame
        self.animation_frame = 0
        self.image = self.frames[self.animation_frame]
        
    def animate(self):
        self.animation_frame += 0.15
        if self.animation_frame >= len(self.frames):
            self.animation_frame = 0
        self.image = self.frames[int(self.animation_frame)]
        
    def update(self, shift):
        self.animate()
        self.rect.x += shift