import pygame
from settings import *
import math

class Echolocation:
    def __init__(self, cover_surf, player):
        self.player = player
        self.cover_surf = cover_surf

        self.echo_radius = 50

        # walking echo management
        self.walking_sound_base_radius = 10
        self.walking_sound_radius = self.walking_sound_base_radius
        self.footstep_timer = 0
        self.footstep_interval = 400
        self.footstep_pulse_amount = 3

    def update_walking_sound(self):
        current_time = pygame.time.get_ticks()

        if self.player.is_moving and not self.player.is_doing_echolocation:
            time_factor = abs(math.sin(current_time / 200))
            self.walking_sound_radius = self.walking_sound_base_radius + (self.footstep_pulse_amount * time_factor)
        else:
            self.walking_sound_radius = self.walking_sound_base_radius

    def draw(self, pos, camera_offset):
        if self.player.is_moving and not self.player.is_doing_echolocation:
            pygame.draw.circle(
                self.cover_surf,
                COLORKEY,
                (pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                self.walking_sound_radius
            )
        elif self.player.is_doing_echolocation:
            pygame.draw.circle(
                self.cover_surf,
                COLORKEY,
                (pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                self.echo_radius
            )
    
    def update(self, pos, camera_offset):
        self.update_walking_sound()
        self.draw(pos, camera_offset)