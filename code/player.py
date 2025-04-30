import pygame
from settings import *
from support import import_character_sprites
from game_mechanics import *

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
    self.is_moving = False
    self.obstacle_sprites = obstacle_sprites

    # echolocation feature
    self.echolocation = Echolocation(self.cover_surf, self)
    self.is_doing_echolocation = False
    self.echolocation_time = 0
    self.echolocation_duration = 4000

    #stats
    self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':2}
    self.health = self.stats['health'] #change health
    self.energy = self.stats['energy'] #chnage energy
    self.exp = 123
    self.speed = self.stats['speed']

    #intergrate with echoloation
    self.energy_recharge_rate = 0.001
    self.energy_drain_rate = 0.007     
    self.max_energy = self.stats['energy']  

    # tracking time
    self.last_update_time = pygame.time.get_ticks()
    self.zero_energy_time = None
    self.echolocation_cooldown_after_zero = 58000
    self.energy_regen_pause_time = 0  # timestamp until which regen is paused
    self.energy_regen_pause_duration = 1000  # 1 second in milliseconds


        

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

    current_time = pygame.time.get_ticks()
    can_use_echolocation = True


    # Check if 1-minute lockout is active
    if self.zero_energy_time is not None:
        if (current_time - self.zero_energy_time) < self.echolocation_cooldown_after_zero:
            can_use_echolocation = False
        else:
            self.zero_energy_time = None  # Reset lockout once time has passed

    if keys[pygame.K_SPACE] and not self.is_doing_echolocation and self.energy > 5 and can_use_echolocation:
        self.is_doing_echolocation = True
        self.echolocation_time = current_time
        self.last_update_time = current_time
        self.echolocation_duration = self.energy * 50  # optional, dynamic duration
        self.energy_regen_pause_time = current_time + self.energy_regen_pause_duration


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
    delta_time = current_time - self.last_update_time

    if self.is_doing_echolocation:
        # Drain energy while using echolocation
        self.energy -= self.energy_drain_rate * delta_time
        self.energy = max(0, self.energy)

        if self.energy <= 5:
            self.energy = 0
            self.is_doing_echolocation = False
            if self.zero_energy_time is None:
               self.zero_energy_time = current_time
        elif (current_time - self.echolocation_time) >= self.echolocation_duration:
            self.is_doing_echolocation = False

    else:
        # Regenerate energy when NOT using echolocation
        # if self.zero_energy_time is None and current_time >= self.energy_regen_pause_time:
              if self.energy < self.max_energy:
                  if current_time >= self.energy_regen_pause_time:
                    self.energy += self.energy_recharge_rate * delta_time
                    self.energy = min(self.energy, self.max_energy)

    self.last_update_time = current_time

    # if (current_time - self.echolocation_time) >= self.echolocation_duration:
    #   self.is_doing_echolocation = False

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

  def update(self):
    self.input()
    self.move(self.speed)
    self.cooldowns()
    self.get_status()
    self.animate()
