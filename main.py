import pygame
import random
import sys
import json

# Константы для направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Глобальные переменные для размеров игрового поля
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

class Snake:
    # Конструктор класса Snake, принимает скорость как параметр
    def __init__(self, speed):
        self.length = 1  # Начальная длина змейки
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]  # Начальное положение
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])  # Направление движения
        self.color = (17, 24, 47)  # Цвет змейки
        self.score = 1  # Начальный счет
        self.speed = speed  # Скорость зависит от сложности

    # Метод возвращает текущую позицию головы змейки
    def get_head_position(self):
        return self.positions[0]

    # Метод для изменения направления движения
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Если направление противоположное, изменение игнорируется
        else:
            self.direction = point  # Изменение направления

    # Метод перемещения змейки
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 1 and new in self.positions[1:]:
            return True  # Если новая позиция уже занята, происходит столкновение
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()  # Удаление последнего элемента, если змейка не растет
        return False

    # Метод для отрисовки змейки на экране
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)  # Границы сегментов

    # Обработка событий клавиатуры для управления змейкой
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food:
    # Конструктор класса Food
    def __init__(self):
        self.position = (0, 0)  # Начальная позиция еды
        self.color = (233, 163, 49)  # Цвет еды
        self.randomize_position()  # Размещение еды в случайной позиции

    # Метод для размещения еды в новой случайной позиции
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    # Метод для отрисовки еды на экране
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)  # Границы сегмента

class Game:
    # Конструктор класса Game
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.display.set_caption("Игра - Змейка")  # Название окна игры
        self.clock = pygame.time.Clock()
        self.load_high_scores()  # Загрузка таблицы рекордов
        speed, difficulty = self.game_intro()  # Запуск начального экрана и выбор сложности
        self.snake = Snake(speed)  # Создание объекта змейки
        self.food = Food()  # Создание объекта еды
        self.difficulty = difficulty  # Сохранение выбранной сложности

    # Метод для загрузки рекордов из файла
    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as file:
                self.high_scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_scores = {}

    # Метод для сохранения рекорда
    def save_high_score(self, new_score, name, difficulty):
        if difficulty not in self.high_scores:
            self.high_scores[difficulty] = []
        self.high_scores[difficulty].append({'name': name, 'score': new_score})
        self.high_scores[difficulty] = sorted(self.high_scores[difficulty], key=lambda x: x['score'], reverse=True)[:5]
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores, file)

    # Метод для вступительного экрана выбора сложности
    def game_intro(self):
        intro = True
        selected_index = 0
        difficulties = ["Легкая", "Средняя", "Тяжелая"]
        speeds = [10, 20, 30]
        while intro:
            self.screen.fill((0, 0, 0))
            self.draw_text('Выберите сложность:', 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5, (255, 255, 255))
            for i, difficulty in enumerate(difficulties):
                color = (0, 255, 0) if i == selected_index else (255, 255, 255)
                self.draw_text(f"{i + 1}. {difficulty}", 24 if i == selected_index else 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 40 * (i + 1), color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(difficulties)
                    elif event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(difficulties)
                    elif event.key == pygame.K_RETURN:
                        intro = False
                        return speeds[selected_index], difficulties[selected_index]
            pygame.display.update()

    # Метод для отрисовки текста на экране
    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        lines = text.split('\n')
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(x, y + i * line_height))
            self.screen.blit(text_surface, text_rect)

    # Экран окончания игры
    def game_over_screen(self, score, difficulty, restart_game):
        current_scores = self.high_scores.get(difficulty, [])
        textbox = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 5, SCREEN_WIDTH // 2, 40)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        font = pygame.font.SysFont('Comic Sans MS', 24)
        while not done:
            self.screen.fill((0, 0, 0))
            self.draw_text(f'Игра окончена! Длинна вашей змейки - {self.snake.score} см \n Введите ваше имя для сложности {difficulty}:', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10)
            for idx, entry in enumerate(current_scores):
                self.draw_text(f'{idx+1}. {entry["name"]} - {entry["score"]}', 18, SCREEN_WIDTH // 2, 180 + 40 * idx)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if textbox.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.save_high_score(score, text, difficulty)
                            text = ''
                            done = True
                        elif event.key == pygame.K_ESCAPE:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            txt_surface = font.render(text, True, (255, 255, 255))
            text_rect = txt_surface.get_rect(center=(textbox.centerx, textbox.centery))
            self.screen.blit(txt_surface, text_rect)
            pygame.draw.rect(self.screen, color, textbox, 2)
            self.draw_button("Рестарт", 50, 400, 'restart', (0, 255, 0), (0, 200, 0), restart_game)
            self.draw_button("Выход", 330, 400, 'exit', (255, 0, 0), (200, 0, 0), sys.exit)
            pygame.display.update()

    # Метод для отрисовки кнопок
    def draw_button(self, text, x, y, id, active_color, inactive_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_width = 100
        button_height = 27
        if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, button_width, button_height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, button_width, button_height))
        self.draw_text(text, 20, x + button_width // 2, y + 10)

    # Основной цикл игры
    def run(self):
        while True:
            self.snake.handle_keys()
            self.draw()
            if self.snake.move():
                self.game_over_screen(self.snake.score, self.difficulty, self.game_restart)
                break
            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.snake.score += 1
                self.food.randomize_position()
            self.clock.tick(self.snake.speed)  # Управление скоростью игры

    # Метод для перезапуска игры
    def game_restart(self):
        game = Game()
        game.run()
        sys.exit()

    # Метод для отрисовки игрового поля и элементов
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_text(f'Длинна змейки: {self.snake.score} см', 20, SCREEN_WIDTH // 2, 10)
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
