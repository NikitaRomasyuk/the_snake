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

    def __init__(self) -> None:
        """Метод инициализации объекта"""
        self.position = None
        self.body_color = None

    def draw(self):
        """метод заглушка для отрисовки"""
        raise NotImplementedError(
            'Определите дочерний'
            'метод draw в %s.' % (self.__class__.__name__))


class Apple(GameObject):
    """Яблочный класс"""

    def __init__(self, color=None):
        """Создание объекта яблока"""
        super().__init__()
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        self.body_color = color

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, filling_cells):
        """Рандомная позиция яблока"""
        retry = True
        while retry:
            random_position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                               randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            if random_position not in filling_cells:
                retry = False
        return random_position


class Snake(GameObject):
    """Класс змеи"""

    length = 1
    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    direction = RIGHT
    growing = False
    next_direction = None
    last_position = None

    def __init__(self, color=None):
        """Инициализация объекта змея"""
        super().__init__()
        self.body_color = color
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Не понимаю как убрать присваивание цвета из данного конструктора

    def reset(self, color=None):
        """Сброс значений объекта, если куснул хвост"""
        self.__init__(color)

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
        self.positions.insert(0, (head_x + x * GRID_SIZE,
                                  head_y + y * GRID_SIZE))
        if not self.growing:
            self.last_position = self.positions[len(self.positions) - 1]
            self.positions.pop(len(self.positions) - 1)
        else:
            self.growing = False

    def window(self):
        """Выход за границу экрана"""
        head_x, head_y = self.get_head_position()
        if head_x == SCREEN_WIDTH:
            self.positions[0] = (0, head_y)
        elif head_x < 0:
            self.positions[0] = (SCREEN_WIDTH, head_y)
        elif head_y == SCREEN_HEIGHT:
            self.positions[0] = (head_x, 0)
        elif head_y < 0:
            self.positions[0] = (head_x, SCREEN_HEIGHT)
        # Не понимаю как применить указанную в ревью формулу
        # coord = head_coord + (direction_coord * GRID_SIZE) %
        # SCREEN_HEIGHT/WIDTH

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
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        apple.draw()
        snake.draw()
        pg.display.update()
        snake.move()
        snake.window()

    # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.growing = True

            apple.position = apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset(SNAKE_COLOR)
            sleep(2)
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
