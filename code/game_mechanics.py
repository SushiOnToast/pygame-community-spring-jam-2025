import pygame
from settings import *
import math

class Echolocation:
    def __init__(self, cover_surf, player):
        self.player = player
        self.cover_surf = cover_surf

        # echolocation wave properties
        self.echo_max_radius = 100
        self.echo_current_radius = 0
        self.echo_speed = 0.5
        self.echo_fade = 255  # Alpha value for echolocation

        # walking echo properties
        self.walking_sound_base_radius = 15
        self.walking_sound_radius = self.walking_sound_base_radius
        self.walking_fade = 255
        self.footstep_interval = 400
        self.footstep_pulse_amount = 5
        self.last_step_time = 0

    def update_walking_sound(self):
        current_time = pygame.time.get_ticks()
        
        if self.player.is_moving and not self.player.is_doing_echolocation:
            # Calculate time since last step
            step_progress = (current_time - self.last_step_time) / self.footstep_interval
            
            if step_progress >= 1:
                self.last_step_time = current_time
                self.walking_sound_radius = self.walking_sound_base_radius
                self.walking_fade = 255
            else:
                # Smooth fade out between steps
                self.walking_fade = max(0, 255 * (1 - step_progress))
                # Gradually increase radius
                self.walking_sound_radius = self.walking_sound_base_radius + (self.footstep_pulse_amount * step_progress)
        else:
            self.walking_fade = max(0, self.walking_fade - 10)  # Fade out when stopping

    def update_echolocation(self):
        if self.player.is_doing_echolocation:
            # Expand the radius
            self.echo_current_radius = min(self.echo_current_radius + self.echo_speed, self.echo_max_radius)
            # Fade out as wave expands
            self.echo_fade = max(0, 255 * (1 - self.echo_current_radius / self.echo_max_radius))
        else:
            self.echo_current_radius = 0
            self.echo_fade = 255

    def draw(self, pos, camera_offset):
        # Create surface for walking sound
        if self.player.is_moving:
            walk_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Convert COLORKEY to RGBA
            color = (*COLORKEY, self.walking_fade)  # Unpack RGB and add alpha
            pygame.draw.circle(
                walk_surf,
                color,
                (pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                self.walking_sound_radius
            )
            self.cover_surf.blit(walk_surf, (0, 0))

        # Create surface for echolocation
        if self.player.is_doing_echolocation:
            echo_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(3):
                radius = self.echo_current_radius - (i * 10)
                if radius > 0:
                    alpha = max(0, self.echo_fade - (i * 50))
                    color = (*COLORKEY, alpha)  # Unpack RGB and add alpha
                    pygame.draw.circle(
                        echo_surf,
                        color,
                        (pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                        radius
                    )
            self.cover_surf.blit(echo_surf, (0, 0))
    
    def update(self, pos, camera_offset):
        self.update_walking_sound()
        self.update_echolocation()
        self.draw(pos, camera_offset)