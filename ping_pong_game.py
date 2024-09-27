# игры на библиотеке pygame
# Назаров ПВ
# pong_game.py

import pygame
from pygame.transform import scale
from random import randint

# Скорость мяча
speed = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = scale(pygame.image.load('Ball_2.png'), (50, 50))
        self.change_x = speed
        self.change_y = speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.x >= 750 or self.rect.x <= 0:
            self.change_x *= -1  # Флип по горизонтали
        if self.rect.y >= 600:
            self.kill()
        if self.rect.y <= 0:
            self.change_y *= -1  # Флип по вертикали
            
        self.rect.x += self.change_x
        self.rect.y += self.change_y

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 120, 20)
        self.image = scale(pygame.image.load("Bar.png"), (120, 20))
        self.xvel = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right):
        if left:
            self.xvel = -speed  # Фиксированная скорость движения
        elif right:
            self.xvel = speed
        else:
            self.xvel = 0

        self.rect.x += self.xvel
        if self.rect.x > 680:
            self.rect.x = 680
        elif self.rect.x < 0:
            self.rect.x = 0

        if self.rect.colliderect(ball.rect):
            ball.change_y *= -1  # Флип по вертикали

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ping-Pong")

sky = scale(pygame.image.load("pong_table.png"), (800, 600))

ship = Spaceship(340, 580)

left = False
right = False

ball = Ball(randint(5, 700), 5)

clock = pygame.time.Clock()

while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                left = True
            if e.key == pygame.K_RIGHT:
                right = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                left = False
            if e.key == pygame.K_RIGHT:
                right = False
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky, (0, 0))
    ship.update(left, right)
    ship.draw(screen)

    ball.update()
    ball.draw(screen)

    pygame.display.update()
    clock.tick(60)  # Ограничение до 60 кадров в секунду
