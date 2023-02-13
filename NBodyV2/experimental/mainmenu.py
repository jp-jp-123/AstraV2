import pygame
import os
import scripthandler
# from pyvidplayer import Video


## creating the window
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")  ## for the caption on top of window

BACKGROUND = pygame.image.load(os.path.join('menu', 'backgrounds', 'splash screen.png'))
TITLE = pygame.image.load(os.path.join('menu', 'texts', 'title.png'))
START = pygame.image.load(os.path.join('menu', 'texts', 'start.png'))
ABOUT = pygame.image.load(os.path.join('menu', 'texts', 'about.png'))
HELP = pygame.image.load(os.path.join('menu', 'texts', 'help.png'))
EXIT = pygame.image.load(os.path.join('menu', 'texts', 'exit.png'))
BACK = pygame.image.load(os.path.join('menu', 'texts', 'back.png'))
BORDER = pygame.image.load(os.path.join('menu', 'texts', 'border.png'))
ICON = pygame.image.load(os.path.join('menu', 'texts', 'splash screen.png'))

ABOUT_PAGE = pygame.image.load(os.path.join('menu', 'backgrounds', 'about page.png'))
HELP_PAGE = pygame.image.load(os.path.join('menu', 'backgrounds', 'help page.png'))

FPS = 80
pygame.display.set_icon(ICON)

##button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False  # variable to prevent multiple click registration
        self.timer = pygame.time.get_ticks()  # get the time when the button was last clicked

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()  # get mouse position
        clicked = pygame.mouse.get_pressed()  # get mouse click status

        if self.rect.collidepoint(pos):  # check if mouse is on the button
            WIN.blit(BORDER, (self.rect.x - 5, self.rect.y + 5))
            # print(self.rect.x, self.rect.y)
            if clicked[0] == 1 and self.clicked == False:  # check if left mouse button is clicked
                current_time = pygame.time.get_ticks()
                if current_time - self.timer == 1:  # check if enough time has passed since last click
                    self.clicked = True
                    self.timer = current_time
                    action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        WIN.blit(self.image, (self.rect.x, self.rect.y))

        return action


# button instances
# vid = Video("menu/backgrounds/astra.MOV")
# vid.set_size((1280, 720))

def main_window():
    pygame.init()

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
            faded_image.set_alpha(alpha)

            # Update the display
            pygame.display.update()

    splash()

    clock = pygame.time.Clock()
    run = True
    state = "home"
    while run:
        if state == "home":
            """def background_vid():
                # background

                vid.draw(WIN, (0, 0), force_draw=False)
                end = vid.active  # tells if the vid is finished
                # restarts the vid when finished = looped bg
                if end == False:
                    print("End")
                    vid.restart()

            background_vid()"""

            WIN.blit(TITLE, (0, 0))
            start_button = Button(540, 230, START)
            help_button = Button(540, 300, HELP)
            about_button = Button(542, 370, ABOUT)
            exit_button = Button(540, 440, EXIT)

            # Buttons
            if start_button.draw():
                state = "start"
            if help_button.draw():
                state = "help"
            if about_button.draw():
                state = "about"
            if exit_button.draw():
                state = "exit"
                run = False

        elif state == "about":
            # background_vid()
            WIN.blit(ABOUT_PAGE, (0, 0))
            back_button = Button(50, 610, BACK)
            if back_button.draw():
                state = "home"

        elif state == "help":
            # background_vid()
            WIN.blit(HELP_PAGE, (0, 0))
            back_button = Button(50, 610, BACK)
            if back_button.draw():
                print('BACK')
                state = "home"

                ## loop for the game whether to quit
        clock.tick(FPS)  ## sets the fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if state == "start":
                    # vid.close()
                    scripthandler.mainSim()
                    run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_window()
