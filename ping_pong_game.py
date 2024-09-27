import pygame
from pygame.transform import scale
from random import randint

# Скорость мяча
speed = 5
speed_bar = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.change_x = speed
        self.change_y = speed
        self.active = True
        self.color = (255, 255, 255)  # Белый цвет для шарика

        self.ball_radius = 20
        self.ball_x = x
        self.ball_y = y
        self.rect = pygame.Rect(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                                self.ball_radius * 2, self.ball_radius * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.ball_x, self.ball_y), self.ball_radius)

    def update(self):
        if not self.active:
            return

        # Обновление координат
        self.ball_x += self.change_x
        self.ball_y += self.change_y

        # Обновление rect
        self.rect.x = self.ball_x - self.ball_radius
        self.rect.y = self.ball_y - self.ball_radius

        if self.ball_x >= 750 or self.ball_x <= 0:
            self.change_x *= -1
        if self.ball_y >= 600:
            self.active = False
        if self.ball_y <= 0:
            self.change_y *= -1


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
            self.xvel = -speed_bar  # Фиксированная скорость движения
        elif right:
            self.xvel = speed_bar
        else:
            self.xvel = 0

        self.rect.x += self.xvel
        if self.rect.x > 680:
            self.rect.x = 680
        elif self.rect.x < 0:
            self.rect.x = 0

        if self.rect.colliderect(ball.rect):
            ball.change_y *= -1  # Флип по вертикали


def reset_game():
    global score, ball
    score = 0
    ball = Ball(randint(5, 700), 5)
    ball.active = True


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ping-Pong")

sky = scale(pygame.image.load("pong_table.png"), (800, 600))

ship = Spaceship(340, 580)

left = False
right = False

ball = Ball(randint(5, 700), 5)
score = 0

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
