from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")


clock = pygame.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self):
        """
        Инициализирует базовые атрибуты объекта:
        позиция и цвет.
        """
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw_cell(self, position):
        """Создание ячейки"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка объекта. По умолчанию pass."""
        pass


class Apple(GameObject):
    """Класс Apple наследуется от GameObject."""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """
        Яблоко появляется со случайными координатами
        в пределах игрового поля
        """
        self.position = (
            (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
            (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT
        )

    def draw(self):
        """Метод draw класса Apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс Snake наследуется от GameObject."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет движение змейки.
        Управляет змейкой в пределах игрового поля.
        """
        head_x, head_y = self.get_head_position()
        xd, yd = self.direction
        x_new = (GRID_SIZE * xd + head_x) % SCREEN_WIDTH
        y_new = (GRID_SIZE * yd + head_y) % SCREEN_HEIGHT

        self.positions.insert(0, (x_new, y_new))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            self.draw_cell(position)

        """Отрисовка головы змейки"""
        self.draw_cell(self.get_head_position())

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP

            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                (game_object.next_direction) = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Вызов функций программы"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.move()
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        pygame.display.update()


if __name__ == "__main__":
    main()
