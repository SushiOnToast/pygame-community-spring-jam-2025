import pygame
from settings import *
import math
from raycasting import *


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

        self.illumination = Illumination()

        # audio
        self.footsteps = pygame.mixer.Sound('graphics/audio/footsteps.wav')
        self.footsteps.set_volume(0.4)
        self.footsteps_channel = pygame.mixer.Channel(1)

    def update_walking_sound(self):
        current_time = pygame.time.get_ticks()

        # Spawn new ripple when stepping
        if self.player.is_moving and not self.player.is_doing_echolocation and not self.player.is_crouching:
            if not self.footsteps_channel.get_busy():
                self.footsteps_channel.play(self.footsteps, loops=-1)
            if current_time - self.last_step_time >= self.footstep_interval:
                self.last_step_time = current_time
                self.walking_ripples.append({
                    'radius': self.walking_sound_base_radius,
                    'alpha': 180
                })
        else:
            # Stop walking sound if not moving or doing echolocation
            if self.footsteps_channel.get_busy():
                self.footsteps_channel.stop()

        # Update existing ripples
        for ripple in self.walking_ripples:
            ripple['radius'] += 0.4  # expand
            ripple['radius'] = min(ripple['radius'], 15)
            ripple['alpha'] = max(0, ripple['alpha'] - 3)  # fade out slowly

        # Remove fully faded ripples
        self.walking_ripples = [
            r for r in self.walking_ripples if r['alpha'] > 0]

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

    def draw(self, pos, camera_offset, points):
        if not self.player.is_crouching:
            # Create surface for walking ripples
            if self.player.is_moving and not self.player.is_doing_echolocation:
                walk_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                for ripple in self.walking_ripples:
                    color = (*COLORKEY, int(ripple['alpha']))
                    pygame.draw.circle(
                        walk_surf,
                        color,
                        (pos.centerx - camera_offset.x,
                         pos.centery - camera_offset.y),
                        ripple['radius'],
                    )
                self.cover_surf.blit(walk_surf, (0, 0))

            # Create surface for echolocation
            if self.player.is_doing_echolocation:
                points = [pygame.Vector2(
                    point) - camera_offset for point in points]
                self.illumination.update((pos.centerx - camera_offset.x, pos.centery - camera_offset.y),
                                         points)
                self.illumination.draw(self.cover_surf)

    def update(self, pos, camera_offset, obstacles):
        self.update_walking_sound()
        self.update_echolocation()
        self.draw(pos, camera_offset, obstacles)


class Illumination:
    def __init__(self):

        self.light_effect = pygame.transform.scale_by(pygame.image.load(
            "graphics/effects/light_effect.png").convert_alpha(), 0.3)
        self.effect_size = self.light_effect.get_size()
        self.pos = None
        self.polygon = []

    def update(self, pos, polygon):
        self.pos = pos
        self.polygon = polygon

    def draw(self, surface):
        if self.pos is not None:
            new_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            if self.polygon:
                pygame.draw.polygon(new_surface, (COLORKEY), self.polygon)
                # for point in self.polygon:
                #     pygame.draw.line(new_surface, (0, 255, 0), self.pos, point)

            new_surface.set_colorkey(COLORKEY)

            effect_pos = (self.pos[0] - self.effect_size[0] // 2,
                          self.pos[1] - self.effect_size[1] // 2)

            surface.blit(self.light_effect, effect_pos)
            surface.blit(new_surface, (0, 0))


class EchoBurst:
    def __init__(self, cover_surf, player):
        self.duration = 1500
