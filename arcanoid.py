# игры на библиотеке pygame
# Назаров ПВ
# arcanoid.py

import pygame
from pygame.transform import scale
from random import randint

# Инициализация Pygame
pygame.init()

# Параметры игры
screen_width = 800
screen_height = 600
block_width = 200
block_height = 40

# Классы
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 15, 15)
        self.change_x = 1 * randint(-1, 1) or 1  # Случайное направление
        self.change_y = -1
        self.color = (255, 255, 0)  # Цвет шара (жёлтый)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.rect.x + 7, self.rect.y + 7), 7)

    def update(self):
        if self.rect.x >= screen_width - 15 or self.rect.x <= 0:
            self.change_x *= -1
        if self.rect.y < 0:
            self.change_y *= -1
        if self.rect.y >= screen_height:
            self.kill()  # Если мяч упал, удаляем его

        self.rect.x += self.change_x
        self.rect.y += self.change_y

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, block_width, block_height)
        self.color = (0, 255, 0)  # Цвет блока (зелёный)
        self.life = 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        if self.rect.colliderect(ball.rect):
            ball.change_y *= -1
            self.life -= 1
            if self.life <= 0:
                self.kill()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 120, 20)
        self.color = (255, 0, 0)  # Цвет щита (красный)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, left, right):
        if left:
            self.rect.x -= 5
        if right:
            self.rect.x += 5
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - 120:
            self.rect.x = screen_width - 120
        if self.rect.colliderect(ball.rect):
            ball.change_y *= -1

# Главная игра
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arkanoid")

ship = Spaceship(340, 580)
ball = Ball(400, 565)

blocks = pygame.sprite.Group()
for i in range(0, screen_width, block_width + 10):
    blocks.add(Block(i, 100))

clock = pygame.time.Clock()
left = False
right = False

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
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

    screen.fill((0, 0, 0))  # Заливка фона
    ship.update(left, right)
    ship.draw(screen)

    ball.update()
    ball.draw(screen)

    blocks.update()
    blocks.draw(screen)

    if ball.rect.y >= screen_height:
        ball = Ball(400, 565)  # Перезапуск мяча

    pygame.display.update()
    clock.tick(60)  # Частота кадров
