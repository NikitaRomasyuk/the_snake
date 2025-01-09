from random import randrange
from time import sleep

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс игры"""

    def __init__(self) -> None:
        """Метод инициализации объекта"""
        self.position = None
        self.body_color = None

    def draw(self):
        """метод заглушка для отрисовки"""
        pass


class Apple(GameObject):
    """Яблочный класс"""

    def __init__(self):
        """Создание объекта яблока"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = Apple.randomize_position(self)

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Рандомная позиция яблока"""
        return (randrange(0, 621, 20), randrange(0, 461, 20))


class Snake(GameObject):
    """Класс змеи"""

    length = 1
    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    direction = RIGHT
    growing = False
    next_direction = None
    last_position = None

    def __init__(self):
        """Инициализация объекта змея"""
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """Поиск головы змея"""
        return self.positions[0]

    def reset(self):
        """Сброс значений объекта, если куснул хвост"""
        sleep(2)
        for position in self.positions[:]:
            last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if (self.next_direction != self.direction
                and self.next_direction is not None):
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змеи"""
        head_x, head_y = self.get_head_position()
        self.positions.insert(0, (head_x + self.direction[0] * GRID_SIZE,
                                  head_y + self.direction[1] * GRID_SIZE))
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

    def draw(self):
        """Рисуем змею"""
        for position in self.positions[:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last_position:
            last_rect = pygame.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(self):
    """Реанируем на кнопки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():
    """Основной метод"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        apple.draw()
        snake.draw()

        pygame.display.update()
        snake.move()
        snake.window()

    # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.growing = True
            head = True
            while head:
                apple.position = apple.randomize_position()
                if apple.position not in snake.positions:
                    head = False
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()


if __name__ == '__main__':
    main()
