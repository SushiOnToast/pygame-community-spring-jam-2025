import pygame, sys
from settings import *
from level import Level
from button import Button
import player
from support import *
from ui import UI
pygame.init()
from debug import debug

#screen
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Spring Gamejam")


class Game:

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing = False
        self.state = "start"

        self.level = Level(self.display_surface)  # Pass display_surface here

    def run(self):
        running = True
        self.state = "running"

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "pause"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw everything to the display surface first
            self.display_surface.fill(BG_COLOR)
            self.level.run()
            
            self.state = self.level.detect_state(self.state)

            if self.state != "running":
                running = False
                self.playing = False

            # Scale the display surface up to the screen
            scaled_surface = pygame.transform.scale_by(self.display_surface, SCALE_FACTOR)
            self.screen.blit(scaled_surface, (0, 0))

            # DRAW UI AFTER SCALING
            self.level.ui.display(self.level.player, self.level.time_survived)

            
            pygame.display.update()
            self.clock.tick(FPS)
def main():
    game = Game()
    run = True
    ui =  UI()

    while run:
        screen.fill(BG_COLOR)  # Background color for menu

        if not game.playing:
            if game.state == "dead":
                exit_clicked = ui.draw_death_screen(screen, game.level.time_survived)
                if exit_clicked:
                    run = False
            else:
                # Draw menu
                start_clicked, exit_clicked = ui.draw_menu(screen, game.state)

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
