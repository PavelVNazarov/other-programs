# игры на библиотеке arcade
# Назаров ПВ
# module_6_pong_game.py

import arcade
#import GL

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong game"


class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('Bar.png', 0.2)

    def update(self):
        if self.right >= SCREEN_WIDTH:
            self.change_x = SCREEN_WIDTH
        if self.left <= 0:
            self.change_x = 0


class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__('Ball.png', 0.05)
        self.change_x += 0.5
        self.change_y += 0.5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right >= SCREEN_WIDTH:
            self.change_x = -self.change_x
        if self.left <= 0:
            self.change_x = -self.change_x
        if self.top >= SCREEN_HEIGHT:
            self.change_y = -self.change_y
        if self.bottom <= 0:
            self.change_y = -self.change_y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bar = Bar()
        self.ball = Ball()
        self.setup()

    def setup(self):
        self.bar.center_x += self.change_x
        self.bar.center_y += self.change_y
        self.ball.center_x += self.change_x
        self.ball.center_y += self.change_y

    def on_draw(self):
        self.clear((255, 255, 255))
        self.bar.draw()
        self.ball.draw()

    def update(self, delta_time):
        if arcade.chek_for_collision(self.bar, self.ball):
            self.ball.change_y = -self.ball.change_y
        self.ball.update()
        self.bar.update()

    def on_key_press(self, key,modifiers):
        if key == arcade.key.RIGHT:
            bar.change_x = 5
        if key == arcade.key.LEFT:
            bar.change_x = -5

    def on_key_release(self, key,modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            bar.change_x = 0


if __name__ == '__main__':
    Window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
