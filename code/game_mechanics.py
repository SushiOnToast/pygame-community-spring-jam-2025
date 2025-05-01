import pygame
from settings import *
import math
from raycasting import get_hit_points


class Echolocation:
    def __init__(self, cover_surf, player):
        self.player = player
        self.cover_surf = cover_surf

        # echolocation wave properties
        self.echo_max_radius = 100
        self.echo_current_radius = 0
        self.echo_speed = 0.5
        self.echo_fade = 255  

        # walking echo properties
        self.walking_sound_base_radius = 1
        self.walking_sound_radius = self.walking_sound_base_radius
        self.walking_fade = 255
        self.footstep_interval = 300
        self.footstep_pulse_amount = 5
        self.last_step_time = 0
        self.walking_ripples = []

    def update_walking_sound(self):
        current_time = pygame.time.get_ticks()

        # Spawn new ripple when stepping
        if self.player.is_moving and not self.player.is_doing_echolocation:
            if current_time - self.last_step_time >= self.footstep_interval:
                self.last_step_time = current_time
                self.walking_ripples.append({
                    'radius': self.walking_sound_base_radius,
                    'alpha': 180  
                })

        # Update existing ripples
        for ripple in self.walking_ripples:
            ripple['radius'] += 0.4  # expand
            ripple['radius'] = min(ripple['radius'], 15)
            ripple['alpha'] = max(0, ripple['alpha'] - 3)  # fade out slowly

        # Remove fully faded ripples
        self.walking_ripples = [r for r in self.walking_ripples if r['alpha'] > 0]


    def update_echolocation(self):
        if self.player.is_doing_echolocation:
            # Expand the radius
            self.echo_current_radius = min(
                self.echo_current_radius + self.echo_speed, self.echo_max_radius)
            # Fade out as wave expands
            self.echo_fade = max(
                0, 255 * (1 - self.echo_current_radius / self.echo_max_radius))
        else:
            self.echo_current_radius = 0
            self.echo_fade = 255
            

    def draw(self, pos, camera_offset, obstacles):
        # Create surface for walking ripples
        if self.player.is_moving and not self.player.is_doing_echolocation:
            walk_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for ripple in self.walking_ripples:
                color = (*COLORKEY, int(ripple['alpha']))
                pygame.draw.circle(
                    walk_surf,
                    color,
                    (pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                    ripple['radius'],
                )
            self.cover_surf.blit(walk_surf, (0, 0))


        # Create surface for echolocation
        if self.player.is_doing_echolocation:
            # echo_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # num_bands = 3 
            # band_spacing = 10  
            # band_thickness = 12  

            # for i in reversed(range(num_bands)):
            #     radius = self.echo_current_radius - (i * band_spacing)
            #     if radius > 0:
            #         alpha = max(0, self.echo_fade -
            #                     ((num_bands - 1 - i) * 40))  
            #         color = (*COLORKEY, alpha)
            #         if i == num_bands-1:
            #             pygame.draw.circle(
            #                 echo_surf,
            #                 color,
            #                 (pos.centerx - camera_offset.x,
            #                 pos.centery - camera_offset.y),
            #                 int(radius),
            #             )
            #         else:
            #             pygame.draw.circle(
            #                 echo_surf,
            #                 color,
            #                 (pos.centerx - camera_offset.x,
            #                 pos.centery - camera_offset.y),
            #                 int(radius),
            #                 width=band_thickness  
            #             )
            # self.cover_surf.blit(echo_surf, (0, 0))
            echo_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            self.echo_fade -= 40
            color = (*COLORKEY, 150)

            # Get hit points in world coordinates
            hit_points = get_hit_points(self.player.hitbox.center, 50, list(obstacles), simplify=True)

            # Convert hit points to screen coordinates using camera offset
            screen_points = [pygame.Vector2(point) - camera_offset for point in hit_points]

            # Draw polygon if valid
            if len(screen_points) >= 3:
                pygame.draw.polygon(echo_surf, color, screen_points)

            self.cover_surf.blit(echo_surf, (0, 0))

    def update(self, pos, camera_offset, obstacles):
        self.update_walking_sound()
        self.update_echolocation()
        self.draw(pos, camera_offset, obstacles)
