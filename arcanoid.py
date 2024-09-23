# игры на библиотеке pygame
# Назаров ПВ
# arcanoid.py

import pygame
from pygame.transform import scale
from random import randint
from time import sleep

speed = 0.005
    # конструктор, в который передаются стартовые координаты
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 15, 15)
        self.image = scale(pygame.image.load('Ball_2.png'), (15, 15))

        self.change_x = 1
        self.change_y = 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.x >= 785:
            self.change_x = -1
        if self.rect.x <= 0:
            self.change_x = 1
        if self.rect.y >= 600:
            self.kill()
        if self.rect.y <= 0:
            self.change_y = 1

        global speed
        #sleep(speed)

        self.rect.x = self.rect.x + self.change_x
        self.rect.y = self.rect.y + self.change_y

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 200, 40)
        self.image = scale(pygame.image.load("Bar.png"), (200, 40))
        self.life = 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.colliderect(ball.rect):
            if ball.change_y > 0:
                ball.change_y = -1
            else:
                ball.change_y = 1
            self.life -= 1
            if self.life <= 0:
                self.kill()
                #del pygameObject_zombie

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
pygame.display.set_caption("Arcanoid")

sky = scale(pygame.image.load("arcanoid_table.png"), (800, 600))
# создаем  в точке 340 580
ship = Spaceship(340, 580)

# заведем переменные, чтобы помнить, какие клавиши нажаты
left = False
right = False

# создаем шарик
ball = Ball(400, 565)
if randint(1,2):
    ball.change_x = 1
else:
    ball.change_x = -1
# блоки
#for i in range(1,11):
block = Block(100,100)
#block2 = Block(400,100)

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

    # перемещаем
    ship.update(left, right)
    # просим  нарисоваться
    ship.draw(screen)

    # шарик

    ball.update()
    ball.draw(screen)

    if block.life > 0:
        block.update()
        block.draw(screen)
    #block2.draw(screen)

    pygame.display.update()
