import pygame
import os
import button
import sys

## creating the window
WIDTH,HEIGHT = 1280,720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Main Menu") ## for the caption on top of window

WHITE = (255,255,255) ## creating variable to easy call colors
# gatherings pictures
BACKGROUND = pygame.image.load(os.path.join('menu','backgroundpic.png'))
TITLE = pygame.image.load(os.path.join('menu','texts','title.png'))
START = pygame.image.load(os.path.join('menu','texts','start.png'))
OPTIONS = pygame.image.load(os.path.join('menu','texts','options.png'))
EXIT = pygame.image.load(os.path.join('menu','texts','exit.png'))
BORDER = pygame.image.load(os.path.join('menu','texts','border.png'))
FPS = 80

##button class
class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False # var. prevents multiple click register 

    def draw(self):
        action = False
        #mouse position
        pos = pygame.mouse.get_pos()
        #print(pos)

        # mouse on button
        if self.rect.collidepoint(pos):
            WIN.blit(BORDER, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # prevents multiple click register
                self.clicked = True
                action = True
        #allows buttons to be re-clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draws button on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def hover(self):
        sense = False
        position = pygame.mouse.get_pos()
        print(position)

        if self.rect.collidepoint(position):
            sense = True
            print('HOVER')



# button instances
start_button = Button (540,280, START,1)
options_button = Button (540,380, OPTIONS,1)
exit_button = Button (540,480,EXIT, 1)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        ## background
        WIN.blit(BACKGROUND,(0,0))
        WIN.blit(TITLE,(0,0))

        # Buttons
        if start_button.draw() == True:
            print('START')
        if options_button.draw() == True:
            print('OPTIONS')
        if exit_button.draw():
            run = False

        ## loop for the game whether to quit
        clock.tick(FPS) ## sets the fps 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

       
       

    pygame.quit()

if __name__=="__main__":
    main()
