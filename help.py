import pygame, sys
import button

pygame.init()

screen_height = 675
screen_width = 1000

background = pygame.image.load('Images/Backgrounds/Help_screen2.png')
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Help")

#loading button image
back_img = pygame.image.load('Images/Backgrounds/back.png').convert_alpha()

#button instances
back_button = button.Button(620,550, back_img)

#game loop
while True:

    #drawing/updating the screen
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    if back_button.draw(screen):
        import Game

# for loop to check game status
    for event in pygame.event.get():
        # Check for QUIT       
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()


