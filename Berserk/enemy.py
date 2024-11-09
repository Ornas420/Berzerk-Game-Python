# enemy.py
import pygame
import random
import time
from bullet import Bullet

ENEMY_COLOR = (255, 0, 0)
ENEMY_SIZE = 20
ENEMY_SPEED = 2

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.last_shot_time = 0
        self.fire_rate = 1.0
    
    def move(self):
        if random.randint(1, 100) > 95:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
        
        if self.direction == 'up':
            self.rect.y -= ENEMY_SPEED
        elif self.direction == 'down':
            self.rect.y += ENEMY_SPEED
        elif self.direction == 'left':
            self.rect.x -= ENEMY_SPEED
        elif self.direction == 'right':
            self.rect.x += ENEMY_SPEED
    
    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)
    
    def player_in_line_of_sight(self, player_rect, walls):
        if abs(self.rect.y - player_rect.y) < 20:
            start_x, end_x = sorted([self.rect.x, player_rect.x])
            return all(not wall.rect.collidepoint(x, self.rect.y) for wall in walls for x in range(start_x, end_x, 20))
        
        elif abs(self.rect.x - player_rect.x) < 20:
            start_y, end_y = sorted([self.rect.y, player_rect.y])
            return all(not wall.rect.collidepoint(self.rect.x, y) for wall in walls for y in range(start_y, end_y, 20))
        
        return False

    def shoot(self, player_rect, walls):
        current_time=time.time()
        if self.player_in_line_of_sight(player_rect, walls) and (current_time - self.last_shot_time) >= self.fire_rate:
            self.last_shot_time = current_time
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            
            if abs(dx) > abs(dy):
                bullet_direction = 'right' if dx > 0 else 'left'
            else:
                bullet_direction = 'down' if dy > 0 else 'up'

            return Bullet(self.rect.centerx, self.rect.centery, bullet_direction)
        return None