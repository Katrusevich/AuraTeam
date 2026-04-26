import pygame
import sys
import random
from logic import Board  # Модуль з логікою
from menu import Menu  # Твій клас меню

# --- КОНСТАНТИ ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
CELL_SIZE = 40
BOARD_SIZE = 10
FPS = 60

# Кольори (запасні, якщо картинки не завантажаться)
BOARD_COLOR = (139, 69, 19)
SEA_COLOR = (44, 62, 80)
TEXT_COLOR = (236, 240, 241)
BTN_COLOR = (52, 152, 219)
READY_COLOR = (46, 204, 113)
HINT_COLOR = (241, 196, 15)


class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        try:
            # Завантажуємо файл (переконайся, що він у папці assets)
            pygame.mixer.music.load("assets/background_music.mp3")

            # Встановлюємо гучність (0.0 до 1.0)
            pygame.mixer.music.set_volume(0.3)

            # Запускаємо відтворення (-1 означає нескінченний повтор)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Помилка завантаження музики: {e}")

        # 1. Екран та шрифти
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("UCUP-2026: Sushi Battle")
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        self.small_font = pygame.font.SysFont("Verdana", 16, bold=True)

        # 2. Завантаження асетів
        self.assets = self._load_assets()

        # 3. Завантаження фону гри (Замість синього кольору)
        try:
            full_bg = pygame.image.load("assets/game_bg.jpg").convert()
            self.game_bg = pygame.transform.scale(full_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.game_bg = None

        # 4. Створення меню
        self.menu = Menu(self.screen, self.font, self.assets)
        self.current_state = "MENU"

        self.clock = pygame.time.Clock()

        # Стан гри
        self.placement_done = False
        self.game_over = False
        self.player_turn = True

        # Кораблі
        self.ships_to_place = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.current_ship_idx = 0
        self.place_direction = 'H'

        # Поля
        self.player_board = Board()
        self.bot_board = Board()
        self._auto_place_ships(self.bot_board)

        self.ai_tried = set()
        self.ai_targets = []

    def _load_assets(self):
        assets = {}
        try:
            board_img = pygame.image.load("assets/board.jpg").convert_alpha()
            assets['board'] = pygame.transform.scale(board_img, (400, 400))
            roll_img = pygame.image.load("assets/roll.png").convert_alpha()
            assets['roll'] = pygame.transform.scale(roll_img, (36, 36))
        except:
            assets['board'] = None
            assets['roll'] = None
        return assets

    def _auto_place_ships(self, board):
        board.clear()
        ship_configs = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for length in ship_configs:
            placed = False
            while not placed:
                r, c = random.randint(0, 9), random.randint(0, 9)
                d = random.choice(['H', 'V'])
                if board.place_ship(length, r, c, d):
                    placed = True

    def draw_button(self, text, x, y, w, h, color):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        if rect.collidepoint(mouse):
            color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)
        txt = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
        return rect

    def draw_grid(self, board, x_offset, y_offset, hide_ships=False):
        # Додаємо легку тінь під дошку для кращої видимості на фоні
        shadow = pygame.Surface((400, 400))
        shadow.set_alpha(80)
        shadow.fill((0, 0, 0))
        self.screen.blit(shadow, (x_offset, y_offset))

        if self.assets['board']:
            self.screen.blit(self.assets['board'], (x_offset, y_offset))
        else:
            pygame.draw.rect(self.screen, BOARD_COLOR, (x_offset, y_offset, 400, 400))

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell_rect = pygame.Rect(x_offset + c * CELL_SIZE, y_offset + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                state = board.grid[r][c]

                if state == Board.SHIP and not hide_ships:
                    if self.assets['roll']:
                        self.screen.blit(self.assets['roll'], (cell_rect.x + 2, cell_rect.y + 2))
                elif state == Board.HIT:
                    pygame.draw.circle(self.screen, (255, 0, 0), cell_rect.center, 14)
                elif state == Board.SUNK:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill((192, 57, 43, 150))
                    self.screen.blit(s, cell_rect)
                elif state == Board.MISS:
                    pygame.draw.circle(self.screen, (60, 30, 10), cell_rect.center, 5)

                pygame.draw.rect(self.screen, (0, 0, 0, 30), cell_rect, 1)

    def bot_logic(self):
        if self.game_over or self.player_turn: return
        pygame.time.delay(600)

        if self.ai_targets:
            r, c = self.ai_targets.pop(0)
        else:
            r, c = random.randint(0, 9), random.randint(0, 9)
            while (r, c) in self.ai_tried:
                r, c = random.randint(0, 9), random.randint(0, 9)

        self.ai_tried.add((r, c))
        res, sunk = self.player_board.receive_shot(r, c)

        if res in ["HIT", "SUNK"]:
            if not sunk:
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.ai_tried:
                        self.ai_targets.append((nr, nc))
            if self.player_board.is_all_sunk(): self.game_over = "STEPASHKA WON!"
            return
        self.player_turn = True

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()

                if self.current_state == "MENU":
                    btn_ai, _, btn_exit = self.menu.draw()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if btn_ai.collidepoint(mx, my):
                            self.current_state = "GAME"
                        elif btn_exit.collidepoint(mx, my):
                            pygame.quit();
                            sys.exit()

                elif self.current_state == "GAME":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.place_direction = 'V' if self.place_direction == 'H' else 'H'

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()

                        if not self.placement_done:
                            # Кнопки UI
                            if 50 <= mx <= 200 and 520 <= my <= 570:
                                self.player_board.clear();
                                self._auto_place_ships(self.player_board)
                                self.current_ship_idx = 10
                            elif 210 <= mx <= 360 and 520 <= my <= 570:
                                self.player_board.clear();
                                self.current_ship_idx = 0
                            elif self.current_ship_idx >= 10 and 425 <= mx <= 625 and 520 <= my <= 580:
                                self.placement_done = True

                            # Розстановка на полі
                            elif self.current_ship_idx < 10:
                                if 300 <= mx < 700 and 100 <= my < 500:
                                    c, r = (mx - 300) // CELL_SIZE, (my - 100) // CELL_SIZE
                                    if self.player_board.place_ship(self.ships_to_place[self.current_ship_idx], r, c,
                                                                    self.place_direction):
                                        self.current_ship_idx += 1

                        elif self.player_turn and not self.game_over:
                            if 550 <= mx < 950 and 100 <= my < 500:
                                c, r = (mx - 550) // CELL_SIZE, (my - 100) // CELL_SIZE
                                if self.bot_board.grid[r][c] in [0, 1]:
                                    res, _ = self.bot_board.receive_shot(r, c)
                                    if res == "MISS": self.player_turn = False
                                    if self.bot_board.is_all_sunk(): self.game_over = "YOU ARE SUSHI MASTER!"

            # МАЛЮВАННЯ
            if self.current_state == "MENU":
                self.menu.draw()

            elif self.current_state == "GAME":
                if self.game_bg:
                    self.screen.blit(self.game_bg, (0, 0))
                else:
                    self.screen.fill(SEA_COLOR)

                if not self.placement_done:
                    self.draw_grid(self.player_board, 300, 100)
                    self.draw_button("AUTO-FILL", 50, 520, 150, 50, BTN_COLOR)
                    self.draw_button("CLEAR ALL", 210, 520, 150, 50, (192, 57, 43))

                    status = f"PLACE {self.ships_to_place[self.current_ship_idx] if self.current_ship_idx < 10 else 0}-CELL ROLL"
                    if self.current_ship_idx >= 10:
                        self.draw_button("START BATTLE", 425, 520, 200, 60, READY_COLOR)
                else:
                    self.draw_grid(self.player_board, 50, 100)
                    self.draw_grid(self.bot_board, 550, 100, hide_ships=True)
                    status = self.game_over if self.game_over else (
                        "YOUR TURN" if self.player_turn else "BOT THINKING...")

                txt = self.font.render(status, True, TEXT_COLOR)
                self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 30))

                if self.placement_done and not self.player_turn and not self.game_over:
                    self.bot_logic()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    GameController().run()