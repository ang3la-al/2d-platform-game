import pygame, sys
import button

#setting screen dimensions
screen_height = 700
screen_width = 1000

#setting screen display and background
background = pygame.image.load('Images/Backgrounds/Title_Screen1.png')
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Zion's Quest")  
  
#loading button images
start_img = pygame.image.load('Images/Backgrounds/Start.png').convert_alpha()
help_img = pygame.image.load('Images/Backgrounds/Help.png').convert_alpha()
leaderboard_img = pygame.image.load('Images/Backgrounds/Leaderboard.png').convert_alpha()
title_img =  pygame.image.load('Images/Backgrounds/Zion.png').convert_alpha()

#creating button instances
start_button = button.Button(170, 210, start_img)
help_button = button.Button(193, 300, help_img)
leaderboard_button = button.Button(158, 390, leaderboard_img)
title_img = button.Button(120, 90, title_img)

#main game loop
while True:

    #updating/drawing onto screen
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    #if buttons clicked, import files
    if start_button.draw(screen) == True:
        import main
    if help_button.draw(screen) == True:
        import help
    if leaderboard_button.draw(screen) == True:
        print('Leaderboard')
    title_img.draw(screen)

#event handler
    for event in pygame.event.get():
        #check if quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()