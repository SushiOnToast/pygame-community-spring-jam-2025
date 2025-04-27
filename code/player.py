import pygame


class Player(pygame.sprite.Sprite):

  def __init__(self, pos, groups, obstacle_sprites):
    super().__init__(groups)

    self.image = pygame.Surface((24, 32))
    self.image.fill("red")
    self.rect = self.image.get_rect(topleft=pos)

    # movement
    self.direction = pygame.math.Vector2()
    self.speed = 3
    self.obstacle_sprites = obstacle_sprites

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

  def update(self):
    self.input()
    self.move(self.speed)
