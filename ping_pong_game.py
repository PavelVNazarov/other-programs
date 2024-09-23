# игры на библиотеке pygame
# Назаров ПВ
# pong_game.py

import pygame
from pygame.transform import scale
from random import randint

# создаем Астероид, расширяющий класс Спрайт

    # конструктор, в который передаются стартовые координаты
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.image = scale(pygame.image.load('Ball_2.png'), (50, 50))

        self.change_x = 0.5
        self.change_y = 0.5
        #self.xvel = 0
        #self.yvel = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.x >= 750:
            self.change_x = -1
        if self.rect.x <= 0:
            self.change_x = 0.5
        if self.rect.y >= 600:
            self.kill()
        if self.rect.y <= 0:
            self.change_y = 0.5

        self.rect.x = self.rect.x + self.change_x
        self.rect.y = self.rect.y + self.change_y

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 120, 20)
        self.image = scale(pygame.image.load("Bar.png"), (120, 20))
        self.xvel = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right):
        if left:
            self.xvel -= 0.1
        if right:
            self.xvel += 0.1
        if not (left or right):
            self.xvel = 0

        if self.rect.x >= 680:
            self.rect.x = 680
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.colliderect(ball.rect):
            ball.change_y = -1
        self.rect.x += self.xvel

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ping-Pong")

sky = scale(pygame.image.load("pong_table.png"), (800, 600))
# создаем корабль в точке 400 400
ship = Spaceship(340, 580)

# заведем переменные, чтобы помнить, какие клавиши нажаты
left = False
right = False

# создаем астероид
ball = Ball(randint(5, 700), 5)

while True:

    for e in pygame.event.get():
        # если нажата клавиша - меняем переменную
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True

        # если отпущена клавиша - меняем переменную
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
           left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
           right = False

        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")

    # рисуем небо
    screen.blit(sky, (0, 0))

    # перемещаем корабль
    ship.update(left, right)
    # просим корабль нарисоваться
    ship.draw(screen)

    # не астероид а шарик

    ball.update()
    ball.draw(screen)

    pygame.display.update()
