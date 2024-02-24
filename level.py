import pygame
from csv import reader
from tiles import *
from enemy import *
from player import *

#defining variables
tile_size = 32

#dictionary for level data
levels = {
    0: {'terrain': 'levels/0/level1_terrain.csv',
        'gems': 'levels/0/level1_gems.csv',
        'fireskull': 'levels/0/level1_fireskull.csv',
        'ghost': 'levels/0/level1_ghost.csv',
        'constraints': 'levels/0/level1_constraints.csv',
        'key': 'levels/0/level1_key.csv',
        'player': 'levels/0/level1_player.csv',
        'position': (500, 225),
        'unlock': 1,
        'choice_images': 'Images/Transition/0.png',},
    1: {'terrain': 'levels/0/level2_terrain.csv',
        'gems': 'levels/0/level2_gems.csv',
        'fireskull': 'levels/0/level2_fireskull.csv',
        'ghost': 'levels/0/level2_ghost.csv',
        'constraints': 'levels/0/level2_constraints.csv',
        'key': 'levels/0/level2_key.csv',
        'player': 'levels/0/level2_player.csv',
        'position': (500, 300),
        'unlock': 2,
        'choice_images': 'Images/Transition/1.png',},
    2: {'terrain': 'levels/0/level3_terrain.csv',
        'gems': 'levels/0/level3_gems.csv',
        'fireskull': 'levels/0/level3_fireskull.csv',
        'ghost': 'levels/0/level3_ghost.csv',
        'constraints': 'levels/0/level3_constraints.csv',
        'key': 'levels/0/level3_key.csv',
        'player': 'levels/0/level3_player.csv',
        'position': (500, 375),
        'unlock': 3,
        'choice_images': 'Images/Transition/2.png',},}

#function for importing csv data
def import_csv(path):
    #list for values of terrain
    terrain_map = []
    #opening and reading the csv file
    with open(path) as map:
        level = reader(map, delimiter = ',')
        #looping through each row
        for row in level:
            #converting rows to a list
            terrain_map.append(list(row))
        return terrain_map

#function for importing and cutting tile graphics
def import_graphics(path):
    #loading image file from path
    surface = pygame.image.load(path).convert_alpha()
    #calculating number of tiles in x,y directions
    tile_x = int(surface.get_size()[0] / tile_size)
    tile_y = int(surface.get_size()[1] / tile_size)
    
    #creating a list for each images
    cut_tiles = []
    #looping through rows adn columns to get images
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * tile_size
            y = row * tile_size
            #creating new surface for tiles, flags = sets unused pixels to invisible
            new_surface = pygame.Surface((tile_size,tile_size), flags = pygame.SRCALPHA)
            #rect = which ration of image to be drawn
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            #adding new tiles to the list
            cut_tiles.append(new_surface)
    return cut_tiles
    
class Level:
    def __init__(self, current_level, surface, create_transition, gem_update, health_update):
        
        self.display_surface = surface  #where to draw onto screen
        self.camera_scroll = 0 #camera scroll
        self.current_x = 0

        #transition
        self.create_transition = create_transition
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max = level_data['unlock']

        #HUD update
        self.gem_update = gem_update
        
        #level sounds
        self.gem_sound = pygame.mixer.Sound('Sound/Gem.mp3')
        self.step_sound = pygame.mixer.Sound('Sound/Stomp.wav')
        
        
                
        #player tiles + defining end goal
        player_layout = import_csv(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, health_update)
        
        #dictionary of layouts, values imported from csv
        tile_layouts = {'terrain': import_csv(level_data['terrain']),
            'gems': import_csv(level_data['gems']),
            'fireskull': import_csv(level_data['fireskull']),
            'ghost': import_csv(level_data['ghost']),
            'constraints': import_csv(level_data['constraints'])}

        #creating sprite groups
        self.terrain_sprites = self.create_tiles(tile_layouts['terrain'], 'terrain')
        self.gem_sprites = self.create_tiles(tile_layouts['gems'], 'gems')
        self.fireskull_sprites = self.create_tiles(tile_layouts['fireskull'], 'fireskull')
        self.ghost_sprites = self.create_tiles(tile_layouts['ghost'], 'ghost')
        self.constraints_sprites = self.create_tiles(tile_layouts['constraints'], 'constraints')

    def create_tiles(self, layout, type):
        #empty sprite group to hold tiles
        sprite_group = pygame.sprite.Group()
        file_path = {
            'terrain': 'Images/TileSet/Tileset.png',
            'gems': 'Images/Collectables/Gems.png'}
        #looping through group to create tiles
        for row_index, row in enumerate(layout):
            for column_index, val in enumerate(row):
                #check csv file value not -1
                if val != '-1':
                    #working out coordinates
                    x = column_index * tile_size
                    y = row_index * tile_size
                    #if terrain/gem, create tile
                    if type in file_path:
                        tiles = import_graphics(file_path[type])
                        tile_surface = tiles[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    #create animated tile for fireskull
                    elif type == 'fireskull':
                        sprite = Fireskull(tile_size, x, y)
                    #create enemy tile for ghost
                    elif type == 'ghost':
                        sprite = Ghost(tile_size, x, y)
                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group
        
    def player_setup(self, layout, health_update):
        #looping through rows/columns to find where to place the player
        for row_index, row in enumerate(layout):
            for column_index, val in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                #if value = 2, place player
                if val == '2':
                    sprite = Player((x,y), health_update)
                    self.player.add(sprite)
                #if value = 3, place goal
                if val == '3':
                    goal_surface = pygame.image.load('Images/Collectables/key.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, goal_surface)
                    self.goal.add(sprite)                        

    def collisions(self):
        player = self.player.sprite
        #updating x coordinate
        player.rect.x += player.direction.x * player.speed
    
        #horizontal collisions
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                     
        #vertical collisions
        player.apply_gravity()    
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0            
                    player.on_ceiling = True
        
        # resetting collisions
        if player.on_left:
            if player.rect.left >= self.current_x:
                player.on_left = False
        if player.on_right:
            if player.rect.right <= self.current_x:
                player.on_right = False
        if player.on_ground:
            if player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
        if player.on_ceiling:
            if player.direction.y > 0:
                player.on_ceiling = False    
    
    def scrolling(self):
        player = self.player.sprite
        #player x position
        player_x = player.rect.centerx
        #player movement direction
        direction_x = player.direction.x
        
        #check if player is near screen edge
        if player_x < 250 and direction_x < 0:
            self.camera_scroll = 5
            player.speed = 0
        elif player_x > 800 and direction_x > 0:
            self.camera_scroll = -5
            player.speed = 0  
        else:
            #reset the camera scroll
            self.camera_scroll = 0
            player.speed = 4           
                        
    def ghost_reverse(self):
        #looping through ghost sprites
        for ghost in self.ghost_sprites.sprites():
            #check collision between constraints
            if pygame.sprite.spritecollide(ghost,self.constraints_sprites,False):
                #reverse direction
                ghost.reverse()
    
    def check_death(self):
        #if player position below 576
        if self.player.sprite.rect.top > 576:
            #call create transition, reset level
            self.create_transition(self.current_level, 0)
    
    def check_goal(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_transition(self.current_level, self.new_max)
            self.gem_sound.play()

    def gem_collection(self):
        #detecting collisions
        collected_gems = pygame.sprite.spritecollide(self.player.sprite,self.gem_sprites,True)
        #if gems collected
        if collected_gems:
            #add 1 to gem count
            for gem in collected_gems:
                self.gem_update(1)
                self.gem_sound.play()
    
    def enemy_collisions(self):
        #checking collision with ghost
        ghost_collide = pygame.sprite.spritecollide(self.player.sprite,self.ghost_sprites,False)
        if ghost_collide:
            for ghost in ghost_collide:
                #setting rect values for collisions
                ghost_center = ghost.rect.center
                ghost_top = ghost.rect.top
                player_bottom = self.player.sprite.rect.bottom
                #if player jumps on enemy, kill it
                if ghost_top < player_bottom < ghost_center[1] and self.player.sprite.direction.y >= 0:
                    self.step_sound.play()
                    #player jumps when kills enemy
                    self.player.sprite.direction.y = -10
                    ghost.kill()
                else:
                    #if collision elsewhere, player takes damage
                    self.player.sprite.calculate_damage()
        
        #checking collision with fireskull
        fireskull_collide = pygame.sprite.spritecollide(self.player.sprite,self.fireskull_sprites,False)
        if fireskull_collide:
            for fireskull in fireskull_collide:
                #if player collides, they take damage
                self.player.sprite.calculate_damage()    

        
    def run(self):
        #drawing/updating terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.camera_scroll)
        
        #drawing/updating gems
        self.gem_sprites.draw(self.display_surface)
        self.gem_sprites.update(self.camera_scroll)

        #drawing/updating firsku;;
        self.fireskull_sprites.draw(self.display_surface)
        self.fireskull_sprites.update(self.camera_scroll)
        
        #drawing/updating ghost
        self.ghost_sprites.draw(self.display_surface)
        self.constraints_sprites.update(self.camera_scroll)
        self.ghost_reverse()
        self.ghost_sprites.update(self.camera_scroll)

        #drawing/updating player
        self.player.update()
        self.player.draw(self.display_surface)
        #checking collisions with terrain
        self.collisions()
        
        #scroll camera based on player pos
        self.scrolling()
        
        #update/draw goal
        self.goal.update(self.camera_scroll)
        self.goal.draw(self.display_surface)

        #check death and key collected
        self.check_death()
        self.check_goal()
        
        #update HUD
        self.gem_collection()
        self.enemy_collisions()