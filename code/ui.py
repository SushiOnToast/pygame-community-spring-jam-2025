import pygame
from settings import *
from button import Button
from support import draw_text


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # menu font
        self.menu_font = pygame.font.Font(
            '../graphics/font/Minecraftia-Regular.ttf', 50)

        # Load button images
        self.start_img = pygame.image.load(
            "../graphics/button/start_btn.png").convert_alpha()
        self.exit_img = pygame.image.load(
            "../graphics/button/exit_btn.png").convert_alpha()
        self.unpause_img = pygame.image.load(
            "../graphics/button/unpause_btn.png"
        ).convert_alpha()

        #win screen
        self.win_image = pygame.image.load("graphics/WhatsApp Image 2025-05-05 at 23.11.24.jpeg").convert_alpha()

        # Create button instances
        self.start_button = Button(WINDOW_WIDTH/2, 320, self.start_img)
        self.unpause_button = Button(WINDOW_WIDTH/2, 320, self.unpause_img)
        self.exit_button = Button(WINDOW_WIDTH/2, 410, self.exit_img)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR,
                         text_rect.inflate(20, 20), 3)

    def display(self, player, time_survived):

        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        draw_text(self.display_surface, str(time_survived), self.menu_font, TEXT_COLOR, WINDOW_WIDTH-50, 50)

    def draw_death_screen(self, screen, time_survived):
        screen.fill(BG_COLOR)
        draw_text(screen, "You died!", self.menu_font, TEXT_COLOR, 465, 100)
        draw_text(screen, str(time_survived), self.menu_font, TEXT_COLOR, 465, 150)
        exit_clicked = self.exit_button.update(screen)

        return exit_clicked
    
    def win_screen(self,screen,state):
        if state == 'win':
            rect = self.win_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(self.win_image, rect)



    def draw_menu(self, screen, state):

        screen.fill(BG_COLOR)  # Background color for menu
        draw_text(screen, "Echospace", self.menu_font, TEXT_COLOR, 465, 100)
        if state == "start":
            start_pause_clicked = self.start_button.update(screen)
        elif state == "pause":
            start_pause_clicked = self.unpause_button.update(screen)

        exit_clicked = self.exit_button.update(screen)

        return start_pause_clicked, exit_clicked
