import pygame
from settings import *
from support import import_character_sprites
from game_mechanics import *
from entity import Entity

class Player(Entity):

  def __init__(self, pos, groups, obstacle_sprites, cover_surf):
    super().__init__(groups)

    self.cover_surf = cover_surf

    # graphics and animation
    self.spritesheet = pygame.image.load(
        "../graphics/player/player.png").convert_alpha()
    self.animations = import_character_sprites(
        self.spritesheet, self.spritesheet.get_width()/4, self.spritesheet.get_height()/4)
    self.status = "down_idle"
 

    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(topleft=pos)

    # movement
    self.hitbox = self.rect.copy()
    self.is_moving = False
    self.obstacle_sprites = obstacle_sprites

    # echolocation feature
    self.echolocation = Echolocation(self.cover_surf, self)
    self.is_doing_echolocation = False
    self.echolocation_time = 0
    self.base_echolocation_duration = 3000  # 4 seconds base duration
    self.echolocation_duration = self.base_echolocation_duration
    self.is_crouching = False

    #stats
    self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':2}
    self.health = self.stats['health'] #change health
    self.health = max(0, self.health)
    self.energy = self.stats['energy'] #chnage energy
    self.exp = 123
    self.speed = self.stats['speed']

    #intergrate with echoloation
    self.energy_recharge_rate = 0.001
    self.energy_drain_rate = 0.003     
    self.max_energy = self.stats['energy']  

    # tracking time
    self.last_update_time = pygame.time.get_ticks()
    self.zero_energy_time = None
    self.echolocation_cooldown_after_zero = 58000
    self.energy_regen_pause_time = 0  # timestamp until which regen is paused
    self.energy_regen_pause_duration = 1000  # 1 second in milliseconds

    self.can_do_echolocation = True
   

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

    if keys[pygame.K_SPACE] and not self.is_doing_echolocation and self.energy > 5 and self.can_do_echolocation:
        self.is_doing_echolocation = True
        self.echolocation_time = pygame.time.get_ticks()
        self.last_update_time = pygame.time.get_ticks()
        # Use fixed duration instead of energy-based
        self.echolocation_duration = self.base_echolocation_duration
        self.energy_regen_pause_time = pygame.time.get_ticks() + self.energy_regen_pause_duration
    
    if keys[pygame.K_LCTRL]:
      self.is_crouching = True
    else:
      self.is_crouching = False

  def cooldowns(self):
      current_time = pygame.time.get_ticks()
      delta_time = current_time - self.last_update_time

      if self.is_doing_echolocation:
          if not hasattr(self, 'echolocation_time'):  # Safety check
              self.echolocation_time = current_time
              
          # Check duration first
          if (current_time - self.echolocation_time) >= self.echolocation_duration:
              self.is_doing_echolocation = False
              self.energy_regen_pause_time = current_time + self.energy_regen_pause_duration
          else:
              # Drain energy while active
              self.energy -= self.energy_drain_rate * delta_time
              if self.energy <= 5:
                  self.energy = 0
                  self.is_doing_echolocation = False
                  self.zero_energy_time = current_time
                  self.can_do_echolocation = False  # Prevent immediate reuse

      else:
          # Energy regeneration
          if current_time >= self.energy_regen_pause_time:
              if self.energy < self.max_energy:
                  self.energy += self.energy_recharge_rate * delta_time
                  self.energy = min(self.energy, self.max_energy)

      # Check cooldown after zero energy
      if self.zero_energy_time is not None:
          if (current_time - self.zero_energy_time) >= self.echolocation_cooldown_after_zero:
              self.zero_energy_time = None
              self.can_do_echolocation = True  # Re-enable echolocation

      self.last_update_time = current_time

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
  
  def update_speed(self):
    speed_multiplier = 1
    animation_speed_multiplier = 1
    if self.is_crouching:
      speed_multiplier = 0.5
      animation_speed_multiplier = 0.5
    
    self.speed = self.stats["speed"] * speed_multiplier
    self.animation_speed = 0.15 * animation_speed_multiplier

  def update(self):
    self.input()
    self.move(self.speed)
    self.cooldowns()
    self.get_status()
    self.animate()
    self.update_speed()
    
