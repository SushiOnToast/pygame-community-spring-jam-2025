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

        #graphics setup
        #self.import_graphics(monster_name)
        self.spritesheet = pygame.image.load(
        "../graphics/player/pixil-frame-0 (9).png").convert_alpha()
        self.animations = import_character_sprites(
            self.spritesheet, self.spritesheet.get_width()/4, self.spritesheet.get_height()/4)
        self.status = "down_idle"
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

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

        self.direction = pygame.math.Vector2()

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
        elif self.status == 'right': #supposed to be left
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

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
        self.get_status(player)
        self.actions(player)

      

        


