import pygame
pygame.init()
font = pygame.font.Font(None, 30)


def debug(surface, info, x=10, y=10):
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(surface, "black", debug_rect)
    surface.blit(debug_surf, debug_rect)

