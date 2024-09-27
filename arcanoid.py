# игры на библиотеке pygame
# Назаров ПВ
# arcanoid.py

import pygame
from pygame.transform import scale
from random import randint
from time import sleep

speed = 0.005

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 15, 15)
        self.change_x = 1
        self.change_y = 1
        self.color = (255, 255, 0)  # Цвет шара (жёлтый)

    def draw(self, screen):
        # Рисуем круг вместо спрайта
        pygame.draw.circle(screen, self.color, (self.rect.x + 7, self.rect.y + 7), 7)  # +7 для центра круга

    def update(self):
        if self.rect.x >= 785:
            self.change_x = -1
        if self.rect.x <= 0:
            self.change_x = 1
        if self.rect.y >= 600:
            self.kill()  # Если мяч упал, удаляем его
        if self.rect.y <= 0:
            self.change_y = 1

        self.rect.x += self.change_x
        self.rect.y += self.change_y

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

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                left = True
            if e.key == pygame.K_RIGHT:
                right = True
            if e.key == pygame.K_q:  # Увеличить скорость
                if speed < 10:
                    speed += 1
                else:
                    speed = 10
            if e.key == pygame.K_s:  # Убавить скорось
                if speed > 2:
                    speed -= 1
                else:
                    speed = 1
            if e.key == pygame.K_r:  # Начать сначала
                reset_game()
            if e.key == pygame.K_n:  # Новая подача
                if ball.active == None:
                    ball = Ball(ship.rect.x + 50, ship.rect.y - 50)
                    ball.active = True
            if e.key == pygame.K_e:  # Закончить игру
                pygame.quit()
                exit()
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
    if ball.active == False:  # Если мяч пропал
        score += 1  # Увеличиваем счет
        ball.active = None
    ball.draw(screen)

    # Вывод счета на экран
    score_text = font.render(f"Пропущенные мячи: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)  # Ограничение до 60 кадров в секунду

    pygame.display.update()
