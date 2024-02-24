import pygame

class HUD:
    def __init__(self,surface):
        #setting display surface
        self.display_surface = surface
        
        #loading health meter image
        self.health_meter = pygame.image.load('Images/red_bar.png').convert_alpha()
        #setting position and size
        self.topleft_bar = (23,27)
        self.max_width = 194
        self.height = 17
       
        #loading gem image
        self.gems = pygame.image.load('Images/Collectables/Gems.png').convert_alpha()
        #setting position
        self.gems_rect = self.gems.get_rect(topleft = (250,20))
        self.font = pygame.font.SysFont(None, 25)
        
    #showing player health bar    
    def show_health(self, current, full):
        #draw health bar onto screen
        self.display_surface.blit(self.health_meter, (20,25))
        #calculate % of health + bar width
        cur_percentage = current / full
        cur_meter_width = self.max_width * cur_percentage
        
        #create rect for health meter + draw onto screen
        health_meter_rect = pygame.Rect((self.topleft_bar),(cur_meter_width,self.height))
        pygame.draw.rect(self.display_surface,'#43b02a',health_meter_rect)
    
    #showing gems collected
    def show_gems(self,amount):
        #draw no. of gems collected onto screen
        self.display_surface.blit(self.gems,self.gems_rect)
        
        #show no. of gems collected + setting its position
        gems_amount_surface = self.font.render(str(amount),False,'white')
        gems_amount_rect = gems_amount_surface.get_rect(midleft = (self.gems_rect.right + 5,self.gems_rect.centery))
        
        #drawing text to screen
        self.display_surface.blit(gems_amount_surface,gems_amount_rect)