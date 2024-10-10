питон пигейм нарисовать движущийся кружок

ИИ: Учим Python
Вот пример простого кода на Python с использованием библиотеки Pygame для создания движущегося круга:

Python
Копировать
import pygame

# Инициализация Pygame
pygame.init()

# Настройка окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Движущийся круг")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры и начальная позиция круга
circle_radius = 50
circle_x = screen_width // 2
circle_y = screen_height // 2
circle_speed_x = 2
circle_speed_y = 2

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление положения круга
    circle_x += circle_speed_x
    circle_y += circle_speed_y

    # Проверка границ экрана
    if circle_x - circle_radius < 0 or circle_x + circle_radius > screen_width:
        circle_speed_x *= -1
    if circle_y - circle_radius < 0 or circle_y + circle_radius > screen_height:
        circle_speed_y *= -1

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование круга
    pygame.draw.circle(screen, WHITE, (int(circle_x), int(circle_y)), circle_radius)

    # Обновление экрана
    pygame.display.flip()

# Выход из Pygame
pygame.quit()
Этот код создает окно с размерами 800x600 пикселей и отображает движущийся белый круг на черном фоне. Круг движется со скоростью 2 пикселя по горизонтали и 2 пикселя по вертикали. Когда круг достигает границ экрана, его направление движения меняется на противоположное.

Основные шаги:

Импортируем библиотеку Pygame.
Инициализируем Pygame.
Настраиваем окно и цвета.
Определяем параметры круга (размер, начальное положение, скорость).
Создаем основной игровой цикл, в котором:
Обрабатываем события, такие как закрытие окна.
Обновляем положение круга.
Проверяем границы экрана и меняем направление движения, если круг достигает края.
Очищаем экран.
Рисуем круг.
Обновляем экран.
Завершаем работу Pygame.
Вы можете легко модифицировать этот код, чтобы изменить размеры, скорость или другие характеристики круга.
