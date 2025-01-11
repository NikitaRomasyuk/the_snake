from random import randrange
from time import sleep

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
RESET = True

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс игры"""

    def __init__(self, color=None) -> None:
        """Метод инициализации объекта"""
        self.position = None
        self.body_color = color

    def draw(self):
        """метод заглушка для отрисовки"""
        raise NotImplementedError(
            'Определите дочерний'
            'метод draw в %s.' % (self.__class__.__name__))


class Apple(GameObject):
    """Яблочный класс"""

    def __init__(self, color=None, filling_cells=[]):
        """Создание объекта яблока"""
        super().__init__(color)
        self.position = self.randomize_position(filling_cells)

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, filling_cells=None):
        """Рандомная позиция яблока"""
        while True:
            random_position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                               randrange(0, SCREEN_HEIGHT, GRID_SIZE))

            if random_position not in filling_cells:
                return random_position


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self, color=None):
        """Инициализация объекта змея"""
        super().__init__(color)
        self.reset()

    def reset(self):
        """Сброс значений объекта, если куснул хвост"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.growing = False
        self.next_direction = None
        self.last_position = None

    def get_head_position(self):
        """Поиск головы змея"""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if (self.next_direction != self.direction
                and self.next_direction is not None):
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змеи"""
        head_x, head_y = self.get_head_position()
        x, y = self.direction
        self.positions.insert(0, ((head_x + (x * GRID_SIZE)) % SCREEN_WIDTH,
                                  (head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT))
        if not self.growing:
            self.last_position = self.positions[len(self.positions) - 1]
            self.positions.pop(len(self.positions) - 1)
        else:
            self.growing = False

    def draw(self):
        """Рисуем змею"""
        for position in self.positions[:]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(),
                            (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last_position:
            last_rect = pg.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(self):
    """Реанируем на кнопки"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pg.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pg.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pg.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():
    """Основной метод"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

    # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.growing = True

            apple.position = apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            sleep(2)
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.move()
        pg.display.update()


if __name__ == '__main__':
    main()
