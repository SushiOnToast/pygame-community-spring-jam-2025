import pygame
from settings import *


class Player(pygame.sprite.Sprite):

  def __init__(self, pos, groups, obstacle_sprites, cover_surf):
    super().__init__(groups)

    self.cover_surf = cover_surf

    self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
    self.rect = self.image.get_rect(topleft=pos)

    # movement
    self.direction = pygame.math.Vector2()
    self.is_moving = False
    self.speed = 2
    self.obstacle_sprites = obstacle_sprites

    # echolocation feature
    self.echo_radius = 50
    self.is_doing_echolocation = False
    self.echolocation_time = 0
    self.echolocation_duration = 2000

    # status
    self.status = "idle"
    self.orientation = "up"

  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
      self.direction.y = -1
    elif keys[pygame.K_s]:
      self.direction.y = 1
    else:
      self.direction.y = 0

    if keys[pygame.K_a]:
      self.direction.x = -1
    elif keys[pygame.K_d]:
      self.direction.x = 1
    else:
      self.direction.x = 0

    if keys[pygame.K_SPACE] and not self.is_doing_echolocation:
      self.is_doing_echolocation = True
      self.echolocation_time = pygame.time.get_ticks()

  def move(self, speed):
    if self.direction.magnitude() != 0:
      self.direction = self.direction.normalize()

    self.rect.x += self.direction.x * speed
    self.collision("horizontal")
    self.rect.y += self.direction.y * speed
    self.collision("vertical")

  def collision(self, direction):
    for sprite in self.obstacle_sprites:
      if sprite.rect.colliderect(self.rect):
        if direction == 'horizontal':
          if self.direction.x > 0:  # moving right
            self.rect.right = sprite.rect.left
          if self.direction.x < 0:  # moving left
            self.rect.left = sprite.rect.right
        if direction == 'vertical':
          if self.direction.y > 0:  # moving down
            self.rect.bottom = sprite.rect.top
          if self.direction.y < 0:  # moving up
            self.rect.top = sprite.rect.bottom

  def cooldowns(self):
    current_time = pygame.time.get_ticks()

    if (current_time - self.echolocation_time) >= self.echolocation_duration:
      self.is_doing_echolocation = False

  def echolocation(self, camera_offset):
    if self.is_doing_echolocation:
        # Draw circle in screen space (accounting for camera position)
        pygame.draw.circle(
            self.cover_surf, 
            COLORKEY,
            (self.rect.centerx - camera_offset.x,
              self.rect.centery - camera_offset.y),
            self.echo_radius
        )

  def update(self):
    self.input()
    self.move(self.speed)
    self.cooldowns()
