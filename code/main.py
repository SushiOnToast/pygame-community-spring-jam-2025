import pygame, sys
from settings import *
from level import Level
import button
import player
pygame.init()

#screen
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Spring Gamejam")

# Font
font = pygame.font.Font('../graphics/font/Minecraftia-Regular.ttf', 50)

# Colors
TEXT_COL = (255, 255, 255)

# Load button images
start_img = pygame.image.load("../graphics/button/start_btn.png").convert_alpha()
exit_img = pygame.image.load("../graphics/button/exit_btn.png").convert_alpha()

# Create button instances
start_button = button.Button(456, 210, start_img, 1.3)
exit_button = button.Button(480, 410, exit_img, 1.3)

# Draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#game varibales
game_paused = False

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.screen = screen
        #self.screen = pygame.display.set_mode((WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR))
        #pygame.display.set_caption('Pygame Spring Gamejam')
        self.clock = pygame.time.Clock()
        self.playing = False

        self.level = Level(self.display_surface)  # Pass display_surface here

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #testing hp
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.level.player.get_health(200)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.level.player.get_damage(200)
                

            # Draw everything to the display surface first
            self.display_surface.fill(BG_COLOR)
            self.level.run()

            # Draw the health bar (and other UI) here
            self.level.player.basic_health(self.display_surface)

            # Scale the display surface up to the screen
            scaled_surface = pygame.transform.scale_by(self.display_surface, SCALE_FACTOR)
            self.screen.blit(scaled_surface, (0, 0))
            
            pygame.display.update()
            self.clock.tick(FPS)
def main():
    game = Game()
    run = True

    while run:
        screen.fill(BG_COLOR)  # Background color for menu

        if not game.playing:
            # Draw menu
            draw_text("Echospace", font, TEXT_COL, 465, 100)

            if start_button.draw(screen):
                game.playing = True

            if exit_button.draw(screen):
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
