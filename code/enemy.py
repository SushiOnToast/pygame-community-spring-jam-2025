import pygame
from settings import *
from entity import Entity
from support import import_character_sprites
import pygame.mixer

class Enemy(Entity):
    def __init__(self, monster_name,pos,groups,obstacle_sprites):
        
        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.source_path = monster_info['sprite_path']

        self.direction = pygame.math.Vector2()

        self.vertical_direction = 1  # 1 means down, -1 means up
        self.vertical_speed = 1
        self.max_float_range = 50  # max pixels to move up/down from original position
        self.float_origin = pos[1]

        #graphics setup
        #self.import_graphics(monster_name)
        self.spritesheet = pygame.image.load(self.source_path).convert_alpha()
        self.animations = import_character_sprites(
            self.spritesheet, self.spritesheet.get_width()/4, self.spritesheet.get_height()/4)
        self.status = "down_idle"
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #attack sound
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.attack_sound.set_volume(0.4)  

        self.last_sound_time = 0  
        self.sound_cooldown = 1000  

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance >0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance,direction)

    def get_status(self,player):

        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = 'right'
        elif distance <= self.notice_radius:
            self.status = 'left'
        else:
            self.status = 'down_idle'

    def actions(self,player):
        #this one needs tweaking
        if self.status == 'up_idle': #supposed to be right
            print('attack')
        elif self.status == 'right' and self.monster_name == 'stalker': #supposed to be left
            self.direction = self.get_player_distance_direction(player)[1]

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.move(self.speed)
        self.animate()

    def enemy_update(self,player):
        if hasattr(self, 'custom_status'):
            self.custom_status(player)
        else:
            self.get_status(player)
            
        if hasattr(self, 'custom_actions'):
            self.custom_actions(player)
        else:
            self.actions(player)

      
class BlindEnemy(Enemy):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__('blind', pos, groups, obstacle_sprites)
        # Add properties for echolocation tracking
        self.target_pos = None
        self.detection_range = 1000
        self.memory_duration = 2000
        self.last_echo_time = 0
        self.stuck_threshold = 5
        self.stuck_timer = 0
        self.stuck_timeout = 1000
        self.last_position = pygame.math.Vector2(pos)
        self.move_speed = 2  # Control movement speed
        self.custom_status = self.get_blind_status
        self.custom_actions = self.blind_actions
        self.current_path = None
        self.last_valid_direction = pygame.math.Vector2()

    def get_blind_status(self, player):
        # Custom status logic for blind enemy
        if self.target_pos:
            self.status = 'right'
        else:
            self.status = 'down_idle'

    def blind_actions(self, player):
        current_time = pygame.time.get_ticks()
        current_pos = pygame.math.Vector2(self.rect.center)

        # Check for new echolocation - Only update if not already moving or closer to player
        if player.is_doing_echolocation and player.last_echolocation_pos:
            echo_pos = pygame.math.Vector2(player.last_echolocation_pos)
            distance_to_echo = echo_pos.distance_to(current_pos)
            
            should_update_target = (
                distance_to_echo <= self.detection_range and 
                (self.target_pos is None or 
                 distance_to_echo < current_pos.distance_to(self.target_pos))
            )
            
            if should_update_target:
                self.target_pos = echo_pos.copy()
                self.last_echo_time = current_time
                self.stuck_timer = 0  # Reset stuck timer for new target

        # Movement behavior
        if self.target_pos and current_time - self.last_echo_time < self.memory_duration:
            target_vec = pygame.math.Vector2(self.target_pos)
            distance_to_target = current_pos.distance_to(target_vec)
            
            if distance_to_target > self.stuck_threshold:
                # Calculate direction vector
                direction = (target_vec - current_pos)
                if direction.length() > 0:
                    self.last_valid_direction = direction.normalize()
                    self.direction = self.last_valid_direction
            else:
                self.target_pos = None
                self.direction = pygame.math.Vector2()
        else:
            # Default floating behavior
            self.direction.x = 0
            self.direction.y = self.vertical_direction

            if self.rect.y > self.float_origin + self.max_float_range:
                self.vertical_direction = -1
            elif self.rect.y < self.float_origin - self.max_float_range:
                self.vertical_direction = 1