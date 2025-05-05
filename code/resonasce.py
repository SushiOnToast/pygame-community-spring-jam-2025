import pygame


class Resonance(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/resonance.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass
