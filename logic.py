# logic.py - Модель даних та логіка "Морського бою"

class Ship:
    def __init__(self, cells):
        self.cells = cells  # Список координат [(r, c), (r, c)...]
        self.hits = []  # Координати влучань
        self.is_dead = False

    def check_shot(self, r, c):
        """Перевіряє влучання в цей корабель."""
        if (r, c) in self.cells and (r, c) not in self.hits:
            self.hits.append((r, c))
            if len(self.hits) == len(self.cells):
                self.is_dead = True
            return True, self.is_dead
        return False, False


class Board:
    # Константи станів клітинок
    EMPTY = 0
    SHIP = 1
    MISS = 2
    HIT = 3
    SUNK = 4

    def __init__(self, size=10):
        self.size = size
        self.clear()  # Ініціалізація порожнього поля

    def clear(self):
        """
        ПОВНЕ ОЧИЩЕННЯ ПОЛЯ.
        Цей метод викликається перед кожною новою розстановкою.
        """
        self.grid = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []

    def can_place_ship(self, cells):
        """Перевіряє валідність позиції (межі та буферна зона 1 клітина)."""
        for r, c in cells:
            # Чи в межах поля?
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False

            # Перевірка оточення 3х3 навколо кожної клітини нового корабля
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.grid[nr][nc] == self.SHIP:
                            return False  # Поруч вже є інший рол
        return True

    def place_ship(self, length, r, c, direction):
        """Розміщує корабель: direction 'H' (горизонт) або 'V' (вертикаль)."""
        cells = []
        for i in range(length):
            nr, nc = (r, c + i) if direction == 'H' else (r + i, c)
            cells.append((nr, nc))

        if self.can_place_ship(cells):
            for nr, nc in cells:
                self.grid[nr][nc] = self.SHIP
            new_ship = Ship(cells)
            self.ships.append(new_ship)
            return True
        return False

    def receive_shot(self, r, c):
        """Обробляє постріл. Повертає (результат, чи потоплено)."""
        # Якщо вже стріляли сюди — нічого не міняємо
        if self.grid[r][c] in [self.MISS, self.HIT, self.SUNK]:
            return "ALREADY_SHOT", False

        if self.grid[r][c] == self.SHIP:
            for ship in self.ships:
                is_hit, is_sunk = ship.check_shot(r, c)
                if is_hit:
                    if is_sunk:
                        # Якщо корабель потонув — міняємо статус усіх його клітин
                        for sr, sc in ship.cells:
                            self.grid[sr][sc] = self.SUNK
                        return "SUNK", True
                    else:
                        self.grid[r][c] = self.HIT
                        return "HIT", False

        self.grid[r][c] = self.MISS
        return "MISS", False

    def is_all_sunk(self):
        """Перевірка на перемогу: чи всі кораблі знищені?"""
        if not self.ships: return False
        return all(ship.is_dead for ship in self.ships)