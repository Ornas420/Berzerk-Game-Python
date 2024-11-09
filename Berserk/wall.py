import pygame
WALL_COLOR = (128, 128, 128)

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface):
        pygame.draw.rect(surface, WALL_COLOR, self.rect)