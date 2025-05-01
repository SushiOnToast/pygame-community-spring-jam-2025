import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()


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