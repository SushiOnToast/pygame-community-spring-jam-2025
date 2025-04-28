import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI


class Level:

  def __init__(self, surface):
    self.display_surface = surface

    # sprite group setup
    self.visible_sprites = YSortCameraGroup(self.display_surface)
    self.obstacle_sprites = pygame.sprite.Group()

    # overlay mask 
    self.cover_surf = pygame.Surface((WIDTH, HEIGHT))
    self.cover_surf.set_alpha(OVERLAY_TRANSPARENCY)

    self.create_map()

    # user interface
    self.ui = UI()

  def create_map(self):
    for row_index, row in enumerate(WORLD_MAP):
      for col_index, col in enumerate(row):
        x = col_index * TILESIZE
        y = row_index * TILESIZE
        if col == 'x':
          Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "test")
        if col == 'p':
          self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.cover_surf)

  def draw_overlay(self):
      self.cover_surf.fill('black')
      self.cover_surf.set_colorkey(COLORKEY)
      
      self.player.echolocation.update(self.player.hitbox, self.visible_sprites.offset)
      
      self.cover_surf.set_alpha(OVERLAY_TRANSPARENCY)
      
      if TESTING_OVERLAY:
        self.display_surface.blit(self.cover_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

  def render(self):
    # separate player and background sprites
    self.visible_sprites.custom_draw(self.player)      
    self.draw_overlay()
    self.visible_sprites.draw_player(self.player)
    
  def run(self):
    self.render()
    self.visible_sprites.update()
    self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # Add these new variables for smooth camera
        self.camera_target = pygame.math.Vector2()
        self.camera_speed = 0.1  

    def custom_draw(self, player):
      # Update camera target position
      target_x = player.rect.centerx - self.half_width
      target_y = player.rect.centery - self.half_height
      self.camera_target = pygame.math.Vector2(target_x, target_y)
      
      # Smoothly move camera to target (lerp)
      self.offset.x += (self.camera_target.x - self.offset.x) * self.camera_speed
      self.offset.y += (self.camera_target.y - self.offset.y) * self.camera_speed
      
      # Draw background sprites first
      for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
          if not isinstance(sprite, Player):
              offset_position = sprite.rect.topleft - self.offset
              self.display_surface.blit(sprite.image, offset_position)

    def draw_player(self, player):
      # Draw player after overlay
      offset_position = player.rect.topleft - self.offset
      self.display_surface.blit(player.image, offset_position)