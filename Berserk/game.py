import pygame
import sys
import time
import random
from wall import *
from bullet import *
from enemy import *

class Game:
    def __init__(self):
        pygame.init()
        
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Berzerk - Python Edition")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.PLAYER_COLOR = (0, 128, 255)
        self.PLAYER_SIZE = 20
        self.PLAYER_SPEED = 5

        # Initialize player
        self.player_x, self.player_y = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        self.player_direction = 'right'

        self.walls = self.create_walls()
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        self.enemy_spawn_delay = 1  # Start with 1 enemy
        self.clock = pygame.time.Clock()

    def create_walls(self):
        return [
            Wall(0, 0, self.SCREEN_WIDTH, 20),
            Wall(0, self.SCREEN_HEIGHT - 20, self.SCREEN_WIDTH, 20),
            Wall(0, 0, 20, self.SCREEN_HEIGHT),
            Wall(self.SCREEN_WIDTH - 20, 0, 20, self.SCREEN_HEIGHT),
            Wall(100, 100, 20, 100),
            Wall(200, 200, 150, 20),
            Wall(500, 300, 20, 150),
            Wall(600, 100, 20, 100),
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = self.player_x + self.PLAYER_SIZE // 2
                    bullet_y = self.player_y + self.PLAYER_SIZE // 2
                    self.bullets.append(Bullet(bullet_x, bullet_y, self.player_direction))

    def update_player_position(self):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.player_x, self.player_y
        if keys[pygame.K_a]:  
            new_x -= self.PLAYER_SPEED
            self.player_direction = 'left'
        if keys[pygame.K_d]: 
            new_x += self.PLAYER_SPEED
            self.player_direction = 'right'
        if keys[pygame.K_w]: 
            new_y -= self.PLAYER_SPEED
            self.player_direction = 'up'
        if keys[pygame.K_s]: 
            new_y += self.PLAYER_SPEED
            self.player_direction = 'down'

        player_rect = pygame.Rect(new_x, new_y, self.PLAYER_SIZE, self.PLAYER_SIZE)
        collision = any(player_rect.colliderect(wall.rect) for wall in self.walls)
        
        if not collision:
            self.player_x, self.player_y = new_x, new_y

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            hit_wall = any(bullet.rect.colliderect(wall.rect) for wall in self.walls)
            hit_enemy = next((enemy for enemy in self.enemies if bullet.rect.colliderect(enemy.rect)), None)

            if hit_wall:
                self.bullets.remove(bullet)
            elif hit_enemy:
                self.bullets.remove(bullet)
                self.enemies.remove(hit_enemy)
            else:
                bullet.draw(self.screen)

        player_rect = pygame.Rect(self.player_x, self.player_y, self.PLAYER_SIZE, self.PLAYER_SIZE)
        for bullet in self.enemy_bullets[:]:
            bullet.move()
            hit_wall = any(bullet.rect.colliderect(wall.rect) for wall in self.walls)
            hit_player = bullet.rect.colliderect(player_rect)

            if hit_wall or hit_player:
                self.enemy_bullets.remove(bullet)
                if hit_player:
                    self.show_end_screen()  # Show end screen when the player dies
                    return
            else:
                bullet.draw(self.screen)

    def update_enemies(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.PLAYER_SIZE, self.PLAYER_SIZE)
        for enemy in self.enemies:
            enemy.move()
            if enemy.rect.colliderect(player_rect):
                self.show_end_screen()  # Show end screen when the player dies
                return
            
            for wall in self.walls:
                if enemy.rect.colliderect(wall.rect):
                    enemy.direction = {
                        'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'
                    }[enemy.direction]
            
            bullet = enemy.shoot(player_rect, self.walls)
            if bullet:
                self.enemy_bullets.append(bullet)

    def draw_objects(self):
        self.screen.fill(self.BLACK)
        pygame.draw.rect(self.screen, self.PLAYER_COLOR, 
                         (self.player_x, self.player_y, self.PLAYER_SIZE, self.PLAYER_SIZE))
        for wall in self.walls:
            wall.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        pygame.display.flip()
    
    def spawn_enemies(self):
        if not self.enemies and (time.time() - self.start_time) > self.enemy_spawn_delay:
            self.enemy_spawn_delay += 1
            new_enemies = []
            for _ in range(self.enemy_spawn_delay):
                x = random.randint(50, self.SCREEN_WIDTH - 50)
                y = random.randint(50, self.SCREEN_HEIGHT - 50)
                new_enemies.append(Enemy(x, y))
            self.enemies = new_enemies

    def show_start_screen(self):
        font = pygame.font.Font(None, 74)
        start_text = font.render("Start", True, self.WHITE)
        quit_text = font.render("Quit", True, self.WHITE)

        start_rect = start_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        quit_rect = quit_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))

        while True:
            self.screen.fill(self.BLACK)
            self.screen.blit(start_text, start_rect)
            self.screen.blit(quit_text, quit_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def show_end_screen(self):
        font = pygame.font.Font(None, 74)
        restart_text = font.render("Restart", True, self.WHITE)
        quit_text = font.render("Quit", True, self.WHITE)

        restart_rect = restart_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        quit_rect = quit_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))

        while True:
            self.screen.fill(self.BLACK)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(quit_text, quit_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        self.reset_game()  # Reset the game state for restart
                        return
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def reset_game(self):
        self.player_x, self.player_y = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        self.player_direction = 'right'
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_spawn_delay = 1  # Reset enemy count to initial value
        self.start_time = time.time()


    def run(self):
        self.show_start_screen()
        self.start_time = time.time()
        while True:
            self.handle_events()
            self.update_player_position()
            self.spawn_enemies()
            self.update_bullets()
            self.update_enemies()
            self.draw_objects()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
