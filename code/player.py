import pygame
from settings import *
from support import import_character_sprites
import math


class Player(pygame.sprite.Sprite):

  def __init__(self, pos, groups, obstacle_sprites, cover_surf):
    super().__init__(groups)

    self.cover_surf = cover_surf

    # graphics and animation
    self.spritesheet = pygame.image.load(
        "../graphics/player/character_spritesheet.png").convert_alpha()
    self.animations = import_character_sprites(
        self.spritesheet, self.spritesheet.get_width()/4, self.spritesheet.get_height()/4)
    self.status = "down_idle"
    self.frame_index = 0
    self.animation_speed = 0.15

    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(topleft=pos)

    # movement
    self.hitbox = self.rect.copy()
    self.direction = pygame.math.Vector2()
    # might be useful for the illumination while walking because of footstep sound
    self.is_moving = False
    self.speed = 2
    self.obstacle_sprites = obstacle_sprites

    # echolocation feature
    self.echo_radius = 50
    self.is_doing_echolocation = False
    self.echolocation_time = 0
    self.echolocation_duration = 2000

    # walking echo management
    self.walking_sound_base_radius = 10
    self.walking_sound_radius = self.walking_sound_base_radius
    self.footstep_timer = 0
    self.footstep_interval = 400
    self.footstep_pulse_amount = 3

    # hp
    self.current_health = 1000
    self.maximum_health = 1000
    self.health_bar_length = 70  # adjust maximum bar lenght
    self.health_ratio = self.maximum_health/self.health_bar_length

  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
      self.direction.y = -1
      self.status = "up"
    elif keys[pygame.K_s]:
      self.direction.y = 1
      self.status = "down"
    else:
      self.direction.y = 0

    if keys[pygame.K_a]:
      self.direction.x = -1
      self.status = "left"
    elif keys[pygame.K_d]:
      self.direction.x = 1
      self.status = "right"
    else:
      self.direction.x = 0

    if keys[pygame.K_SPACE] and not self.is_doing_echolocation:
      self.is_doing_echolocation = True
      self.echolocation_time = pygame.time.get_ticks()

  def move(self, speed):
      if self.direction.magnitude() != 0:
        self.direction = self.direction.normalize()

        # Move the hitbox instead of rect
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")

        # Update rect to match hitbox position
        self.rect.center = self.hitbox.center

  def collision(self, direction):
      for sprite in self.obstacle_sprites:
          if sprite.rect.colliderect(self.hitbox):  # Use hitbox for collision
              if direction == 'horizontal':
                  if self.direction.x > 0:  # moving right
                      self.hitbox.right = sprite.rect.left
                  if self.direction.x < 0:  # moving left
                      self.hitbox.left = sprite.rect.right
              if direction == 'vertical':
                  if self.direction.y > 0:  # moving down
                      self.hitbox.bottom = sprite.rect.top
                  if self.direction.y < 0:  # moving up
                      self.hitbox.top = sprite.rect.bottom

  def cooldowns(self):
    current_time = pygame.time.get_ticks()

    if (current_time - self.echolocation_time) >= self.echolocation_duration:
      self.is_doing_echolocation = False

  def update_walking_sound(self):
    current_time = pygame.time.get_ticks()

    if self.is_moving and not self.is_doing_echolocation:
      time_factor = abs(math.sin(current_time / 200))
      self.walking_sound_radius = self.walking_sound_base_radius + (self.footstep_pulse_amount * time_factor)
    else:
      # When not moving, gradually return to base radius
      self.walking_sound_radius = max(self.walking_sound_base_radius, self.walking_sound_radius - 0.5)

  def echolocation(self, camera_offset):
    if self.is_moving and not self.is_doing_echolocation:
       # draw a faint illumination aroudn due to the sound of footsteps, will sync to audio later
       pygame.draw.circle(
            self.cover_surf,
           COLORKEY,
           (self.hitbox.centerx - camera_offset.x,
             self.hitbox.centery - camera_offset.y),
           self.walking_sound_radius
           )
    elif self.is_doing_echolocation:
        # Draw circle in screen space (accounting for camera position)
        pygame.draw.circle(
            self.cover_surf,
            COLORKEY,
            (self.hitbox.centerx - camera_offset.x,
             self.hitbox.centery - camera_offset.y),
            self.echo_radius
        )

  def get_status(self):
    if self.direction.x == 0 and self.direction.y == 0:
      self.is_moving = False
      if not "_idle" in self.status:
        self.status = self.status + "_idle"
    else:
      self.is_moving = True

  def animate(self):
      animation = self.animations[self.status]

      self.frame_index += self.animation_speed
      if self.frame_index >= len(animation):
          self.frame_index = 0

      self.image = animation[int(self.frame_index)]
      self.rect = self.image.get_rect(center=self.hitbox.center)

  def get_damage(self, amount):
    if self.current_health >0:
      self.current_health -= 50  # change to amount
    if self.current_health <= 0:
       self.current_health = 0

  def get_health(self, amount):
    if self.current_health < self.maximum_health:
       self.current_health += 50  # change to amount later
    if self.current_health >= self.maximum_health:
       self.current_health = self.maximum_health

  def basic_health(self, surface):
    health_width = (self.current_health / self.maximum_health) * self.health_bar_length
    health_width = max(0, min(health_width, self.health_bar_length))  # doesn't overflow the max length
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, self.health_bar_length, 5), 4)
    pygame.draw.rect(surface, (0, 128, 0), (10, 10, health_width, 5))

  def update(self):
    self.input()
    self.move(self.speed)
    self.cooldowns()
    self.get_status()
    self.animate()
    self.update_walking_sound()
    self.basic_health(self.cover_surf)
