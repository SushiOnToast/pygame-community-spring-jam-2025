import pygame, sys
from settings import *
from level import Level
from button import Button
import player
from support import *
from ui import UI
pygame.init()

#screen
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Spring Gamejam")

# Font
font = pygame.font.Font('../graphics/font/Minecraftia-Regular.ttf', 50)

# Load button images
start_img = pygame.image.load("../graphics/button/start_btn.png").convert_alpha()
exit_img = pygame.image.load("../graphics/button/exit_btn.png").convert_alpha()

# Create button instances
start_button = Button(456, 210, start_img, 1.3)
exit_button = Button(480, 410, exit_img, 1.3)

#game varibales
game_paused = False

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing = False

        self.level = Level(self.display_surface)  # Pass display_surface here

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
         
                

            # Draw everything to the display surface first
            self.display_surface.fill(BG_COLOR)
            self.level.run()


            # Scale the display surface up to the screen
            scaled_surface = pygame.transform.scale_by(self.display_surface, SCALE_FACTOR)
            self.screen.blit(scaled_surface, (0, 0))

            # DRAW UI AFTER SCALING
            self.level.ui.display(self.level.player)
            
            pygame.display.update()
            self.clock.tick(FPS)
def main():
    game = Game()
    run = True
    ui =  UI()

    while run:
        screen.fill(BG_COLOR)  # Background color for menu

        if not game.playing:
            # Draw menu
            start_clicked, exit_clicked = ui.draw_menu(screen)

            if start_clicked:
                game.playing = True

            if exit_clicked:
                run = False

        else:
            # Run game
            game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        game.clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
