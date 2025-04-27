import pygame
from settings import *
from support import import_character_sprites


class Player(pygame.sprite.Sprite):

  def __init__(self, pos, groups, obstacle_sprites, cover_surf):
    super().__init__(groups)

    self.cover_surf = cover_surf

    # graphics and animation
    self.spritesheet = pygame.image.load("../graphics/player/character_spritesheet.png").convert_alpha()
    self.animations = import_character_sprites(self.spritesheet, self.spritesheet.get_width()/4, self.spritesheet.get_height()/4)
    self.status = "down_idle"
    self.frame_index = 0
    self.animation_speed = 0.15

    self.image = self.animations[self.status][self.frame_index]
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

  def get_status(self):
    if self.direction.x == 0 and self.direction.y == 0:
      if not "_idle" in self.status:
        self.status = self.status + "_idle"

  def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

  def update(self):
    self.input()
    self.move(self.speed)
    self.cooldowns()
    self.get_status()
    self.animate()
