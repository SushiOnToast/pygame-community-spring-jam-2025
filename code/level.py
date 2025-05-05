import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI
from enemy import *
from raycasting import *
from support import *
from resonasce import Resonance
from finalcore import FinalResonance


class Level:

  def __init__(self, surface):
    self.display_surface = surface
    self.time_survived = 0
    self.start_time = pygame.time.get_ticks()

    self.level_index = 1

    # overlay mask
    self.cover_surf = pygame.Surface((WIDTH, HEIGHT))
    self.cover_surf.set_alpha(OVERLAY_TRANSPARENCY)

    self.create_map()

    # user interface
    self.ui = UI()

    self.last_damage_time = pygame.time.get_ticks()

    self.last_switch_time = 0
    self.switch_cooldown = 500  # milliseconds

  def create_map(self):
    self.visible_sprites = YSortCameraGroup(self.display_surface, self.level_index)
    self.obstacle_sprites = pygame.sprite.Group()

    layouts = {
        "boundary1": import_csv_layout("map/boundary1.csv"),
        "boundary2": import_csv_layout("map/boundary2.csv"),
        "boundary3": import_csv_layout("map/boundary3.csv"),
    }

    for row_index, row in enumerate(layouts[f"boundary{self.level_index}"]):
      for col_index, col in enumerate(row):
        x = col_index * TILESIZE
        y = row_index * TILESIZE
        if col == "295":
          self.player = Player(
            (x, y), [self.visible_sprites], self.obstacle_sprites, self.cover_surf)
        if col == '1':
          Enemy('stalker', (x, y), [
                self.visible_sprites], self.obstacle_sprites)
        if col == '2':
          BlindEnemy((x, y), [self.visible_sprites], self.obstacle_sprites)
        if col != "-1" and col != "295" and col != "1" and col != "2" and col!= '200' and col!='202':
          Tile((x, y), [self.obstacle_sprites], "invisible")
        if col == '200':
           self.resonance = Resonance((x,y),[self.visible_sprites])
        if col =='202' and self.level_index == 3:
           self.finalresonance = FinalResonance((x,y),[self.visible_sprites])

  def switch_room(self):
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    if pygame.sprite.collide_rect(self.player, self.resonance):
        self.level_index = (self.level_index % 3) + 1  # Cycle between 1-3
        self.last_switch_time = current_time
        self.create_map()

    
        
  def get_raycasting_points(self, obstacles):
    obstacle_rects = [obstacle.rect for obstacle in obstacles]
    edges = get_all_relevant_edges(obstacle_rects)

    # Corrected: apply camera offset to edge lines
    for edge in edges:
        start = pygame.Vector2(edge[0]) - self.visible_sprites.offset
        end = pygame.Vector2(edge[1]) - self.visible_sprites.offset

    # Apply camera offset to raycasting points
    points = Raycaster.find_all_intersects(self.player.hitbox, edges)

    return points

  def draw_overlay(self):
    self.cover_surf.fill('black')
    self.cover_surf.set_colorkey(COLORKEY)

    points = self.get_raycasting_points(self.obstacle_sprites)
    self.player.echolocation.update(
        self.player.hitbox, self.visible_sprites.offset, points)

    self.cover_surf.set_alpha(OVERLAY_TRANSPARENCY)

    if TESTING_OVERLAY:
      self.display_surface.blit(
          self.cover_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

  # collison thing
  def check_player_enemy_collisions(self):
    current_time = pygame.time.get_ticks()

    if not hasattr(self, 'last_damage_time'):
        self.last_damage_time = current_time
    if not hasattr(self, 'damage_interval'):
        self.damage_interval = 50  # ms between each damage tick
    if not hasattr(self, 'damage_rate'):
        self.damage_rate = 0.005  # damage per ms per attack_damage

    delta_time = current_time - self.last_damage_time

    if delta_time >= self.damage_interval:
      for sprite in self.visible_sprites:
        if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
            if self.player.hitbox.colliderect(sprite.hitbox):
                damage = sprite.attack_damage * self.damage_rate * delta_time
                if self.player.is_crouching and sprite.monster_name == "blind":
                   pass
                else:
                  self.player.health -= damage
                  self.player.health = max(0, self.player.health)

                  now = pygame.time.get_ticks()
                  if hasattr(sprite, 'attack_sound'):
                      if now - sprite.last_sound_time > sprite.sound_cooldown:
                          sprite.attack_sound.play()
                          sprite.last_sound_time = now

      self.last_damage_time = current_time

  def render(self):
    # separate player and background sprites
    # doesnt work because scroll is still needed
    self.visible_sprites.custom_draw(self.player)
    self.draw_overlay()
    self.visible_sprites.draw_player(self.player)
    if self.player.last_echolocation_pos and SHOW_ECHOLOCATION_POINT:
      pygame.draw.circle(self.display_surface, "red", pygame.Vector2(
          self.player.last_echolocation_pos) - self.visible_sprites.offset, 5)

  def update_time_survived(self):
     current_time = pygame.time.get_ticks()
     self.time_survived = (current_time - self.start_time)/1000

  def detect_state(self, current_state):
    state = current_state
    if current_state == "running":
      if self.player.health <= 0:
          state = "dead"
      # if pygame.sprite.collide_rect(self.player, self.resonance):
      #     state = "nextlevel"
      if hasattr(self, 'finalresonance') and pygame.sprite.collide_rect(self.player, self.finalresonance):
         state = "win"
    
      

    return state

  def run(self):
    self.switch_room()
    self.render()
    self.visible_sprites.update()
    self.visible_sprites.enemy_update(self.player)
    self.check_player_enemy_collisions()
    self.update_time_survived()
    self.ui.display(self.player, self.time_survived)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, surface, level_index):
        super().__init__()
        self.display_surface = surface
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.camera_target = pygame.math.Vector2()
        self.camera_speed = 0.1

        # Pre-load and convert floor surface
        self.floor_surface = pygame.image.load(f"graphics/map/map{level_index}.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        
        # Cache for sprite sorting
        self.sorted_sprites = []
        self.last_update_time = 0
        self.sort_interval = 100  # Sort every 100ms

    def custom_draw(self, player):
        # Update camera target position
        self.camera_target.x = player.rect.centerx - self.half_width
        self.camera_target.y = player.rect.centery - self.half_height

        # Use integer positions for smoother rendering
        self.offset.x += (self.camera_target.x - self.offset.x) * self.camera_speed
        self.offset.y += (self.camera_target.y - self.offset.y) * self.camera_speed
        offset_int = pygame.math.Vector2(int(self.offset.x), int(self.offset.y))

        # Draw floor
        floor_offset_pos = self.floor_rect.topleft - offset_int
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # Update sprite sorting only periodically
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.sort_interval:
            self.sorted_sprites = sorted(
                [sprite for sprite in self.sprites() if not isinstance(sprite, Player)],
                key=lambda sprite: sprite.rect.centery
            )
            self.last_update_time = current_time

        # Draw sprites using cached sorting
        for sprite in self.sorted_sprites:
            offset_position = sprite.rect.topleft - offset_int
            self.display_surface.blit(sprite.image, offset_position)

    def draw_player(self, player):
      # Draw player after overlay
      offset_position = player.rect.topleft - self.offset
      self.display_surface.blit(player.image, offset_position)

    def enemy_update(self, player):
      enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
          sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
      for enemy in enemy_sprites:
        enemy.enemy_update(player)
