# bullet.py
import pygame

BULLET_COLOR = (255, 0, 0)
BULLET_SPEED = 5
BULLET_SIZE = 5

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)
        self.direction = direction
    
    def move(self):
        if self.direction == 'up':
            self.rect.y -= BULLET_SPEED
        elif self.direction == 'down':
            self.rect.y += BULLET_SPEED
        elif self.direction == 'left':
            self.rect.x -= BULLET_SPEED
        elif self.direction == 'right':
            self.rect.x += BULLET_SPEED
    
    def draw(self, surface):
        pygame.draw.rect(surface, BULLET_COLOR, self.rect)
    