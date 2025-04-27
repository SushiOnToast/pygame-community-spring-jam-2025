import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode((WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR))
        pygame.display.set_caption('Pygame Spring Gamejam')
        self.clock = pygame.time.Clock()

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
            
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()