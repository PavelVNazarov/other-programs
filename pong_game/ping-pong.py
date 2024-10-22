import pygame
from pygame.transform import scale
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ping-Pong")
button_font = pygame.font.Font(None, 24)

def draw_button(text, pos):
    button_surface = button_font.render(text, True, (255, 255, 255))
    screen.blit(button_surface, pos)

def button_rect(pos):
    return pygame.Rect(pos[0], pos[1], 120, 40)

speed = 5
score = 0
ball = None
ball_served = False  # Флаг для отслеживания подачи мяча

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.change_x = speed
        self.change_y = speed
        self.active = True
        self.color = (255, 255, 255)
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
        self.ball_x += self.change_x
        self.ball_y += self.change_y
        self.rect.x = self.ball_x - self.ball_radius
        self.rect.y = self.ball_y - self.ball_radius
        if self.ball_x >= 750 or self.ball_x <= 0:
            self.change_x *= -1
        if self.ball_y >= 600:
            self.active = False  # Мяч пропущен
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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.xvel = -speed
        elif keys[pygame.K_RIGHT]:
            self.xvel = speed
        else:
            self.xvel = 0

        self.rect.x += self.xvel
        if self.rect.x > 680:
            self.rect.x = 680
        elif self.rect.x < 0:
            self.rect.x = 0

        if self.rect.colliderect(ball.rect):
            ball.change_y *= -1

def reset_game():
    global score, ball, ball_served
    score = 0
    ball_served = False
    ball.active = True

ball = Ball(randint(5, 700), 5)
ship = Spaceship(340, 580)
sky = scale(pygame.image.load("pong_table.png"), (800, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect((10, 50)).collidepoint(mouse_pos):
                if speed < 10:
                    speed += 1
            if button_rect((10, 100)).collidepoint(mouse_pos):
                if speed > 2:
                    speed -= 1
            if button_rect((10, 150)).collidepoint(mouse_pos):
                reset_game()
            if button_rect((10, 200)).collidepoint(mouse_pos):
                if not ball_served:
                    ball = Ball(ship.rect.x + 50, ship.rect.y - 50)
                    ball.active = True
                    ball_served = True
            if button_rect((10, 250)).collidepoint(mouse_pos):
                pygame.quit()
                exit()

    screen.blit(sky, (0, 0))  # Рисуем стол
    if ball.active:
        ball.update()
    ship.update()
    ship.draw(screen)
    if ball.active:
        ball.draw(screen)
        if not ball_served and ball.active == False:
            score += 1
            ball_served = False
    else:
        if not ball_served:
            score_text = button_font.render(f"Пропущенные мячи: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

    score_text = button_font.render(f"Пропущенные мячи: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.draw.rect(screen, (200, 0, 0), button_rect((10, 50)))
    draw_button("Увеличить скорость", (15, 55))
    pygame.draw.rect(screen, (200, 0, 0), button_rect((10, 100)))
    draw_button("Уменьшить скорость", (15, 105))
    pygame.draw.rect(screen, (200, 0, 0), button_rect((10, 150)))
    draw_button("Начать сначала", (15, 155))
    pygame.draw.rect(screen, (200, 0, 0), button_rect((10, 200)))
    draw_button("Новая подача", (15, 205))
    pygame.draw.rect(screen, (200, 0, 0), button_rect((10, 250)))
    draw_button("Закончить игру", (15, 255))

    pygame.display.update()
    clock.tick(60)
