import pygame
import os
from pyvidplayer import Video
import time

## creating the window
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")  ## for the caption on top of window

WHITE = (255, 255, 255)  ## creating variable to easy call colors
# gatherings pictures
BACKGROUND = pygame.image.load(os.path.join('menu', 'texts', 'splash screen.png'))
TITLE = pygame.image.load(os.path.join('menu', 'texts', 'title.png'))
START = pygame.image.load(os.path.join('menu', 'texts', 'start.png'))
OPTIONS = pygame.image.load(os.path.join('menu', 'texts', 'options.png'))
EXIT = pygame.image.load(os.path.join('menu', 'texts', 'exit.png'))
BORDER = pygame.image.load(os.path.join('menu', 'texts', 'border.png'))
FPS = 80


##button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False  # var. prevents multiple click register

    def draw(self):
        action = False
        # mouse position
        pos = pygame.mouse.get_pos()
        # print(pos)

        # mouse on button
        if self.rect.collidepoint(pos):
            WIN.blit(BORDER, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # prevents multiple click register
                self.clicked = True
                action = True
        # allows buttons to be re-clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draws button on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        return action


# button instances
vid = Video("menu/astra.MOV")
vid.set_size((1280, 720))


def main_window():
    def splash():
        # Make a copy of the image to use as the faded version
        faded_image = BACKGROUND.copy()

        # Set the alpha value of the faded image to 0 (completely transparent)
        faded_image.set_alpha(0)

        # Keep track of the current alpha value
        alpha = 0

        # Set the speed at which the image should fade
        fade_speed = 5

        # Fade the image in
        fading_in = True

        fade = True
        while fade == True:
            # Clear the screen
            WIN.fill((0, 0, 0))

            # Draw the faded image on the screen
            WIN.blit(faded_image, (0, 0))

            # Update the alpha value of the faded image
            if fading_in:
                alpha += fade_speed
                if alpha >= 255:
                    alpha = 255
                    fading_in = False

            else:
                alpha -= fade_speed
                if alpha <= 0:
                    alpha = 0
                    fade = False
                    loop = False
            faded_image.set_alpha(alpha)

            # Update the display
            pygame.display.update()

    splash()

    clock = pygame.time.Clock()
    run = True

    while run:
        ## background
        vid.draw(WIN, (0, 0))
        end = vid.active  # tells if the vid is finished
        # print(count)

        # restarts the vid when finished = looped bg
        if end == False:
            # print("End")
            vid.restart()
        # else:
        #    print("Start")

        WIN.blit(TITLE, (0, 0))
        start_button = Button(540, 280, START)
        options_button = Button(540, 380, OPTIONS)
        exit_button = Button(540, 480, EXIT)

        # Buttons
        if start_button.draw() == True:
            print('START')
        if options_button.draw() == True:
            print('OPTIONS')
        if exit_button.draw():
            run = False

        ## loop for the game whether to quit
        clock.tick(FPS)  ## sets the fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # vid.close()
                exit()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_window()
