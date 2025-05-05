import pygame
from settings import *

class Button():
    def __init__(self, x, y, image, scale=7):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        
        # hover properties with transition
        self.hovering = False
        self.current_scale = 1.0
        self.target_scale = 1.0
        self.hover_scale = 1.1
        self.scale_speed = 0.2  # Adjust this to control transition speed (0.1 = slower, 0.3 = faster)
        self.last_update = pygame.time.get_ticks()

    def update_scale(self):
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_update) / 1000.0  # Convert to seconds
        self.last_update = current_time

        # Smoothly interpolate current_scale towards target_scale
        if self.current_scale != self.target_scale:
            diff = self.target_scale - self.current_scale
            self.current_scale += diff * self.scale_speed * dt * 60

    def input(self):
        self.action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hovering = True
            self.target_scale = self.hover_scale
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
        else:
            self.hovering = False
            self.target_scale = 1.0

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def draw(self, surface):
        # Get the scaled image size
        scaled_btn = pygame.transform.scale_by(self.image, self.current_scale)
        scaled_rect = self.rect.copy()
        
        # Center the scaled image on the original position
        scaled_rect.width = scaled_btn.get_width()
        scaled_rect.height = scaled_btn.get_height()
        scaled_rect.center = self.rect.center
        
        surface.blit(scaled_btn, scaled_rect)

    def update(self, surface):
        self.input()
        self.update_scale()
        self.draw(surface)
        return self.action