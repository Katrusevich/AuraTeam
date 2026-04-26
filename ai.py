# ai.py - Інтелект бота Stepashka
import random


class BotStepashka:
    def __init__(self, board_size=10):
        self.size = board_size
        self.tried_cells = set()  # Клітини, куди вже стріляли
        self.target_queue = []  # Черга пріоритетних цілей (Target Mode)
        self.last_hit = None  # Остання клітина влучання

    def get_shot_coordinates(self):
        """Вибирає координати для наступного пострілу."""
        # Режим TARGET: якщо є черга потенційних цілей навколо влучання
        if self.target_queue:
            shot = self.target_queue.pop(0)
            while shot in self.tried_cells:
                if not self.target_queue:
                    return self._hunt_random()
                shot = self.target_queue.pop(0)
            return shot

        # Режим HUNT: випадковий постріл у шаховому порядку для ефективності
        return self._hunt_random()

    def _hunt_random(self):
        """Рандомний постріл (можна додати логіку шахової дошки)."""
        while True:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if (r, c) not in self.tried_cells:
                return (r, c)

    def process_feedback(self, r, c, result):
        """
        Отримує фідбек про результат пострілу.
        result: "MISS", "HIT", або "SUNK"
        """
        self.tried_cells.add((r, c))

        if result == "HIT":
            # Додаємо сусідні клітини до черги (Target Mode)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in self.tried_cells:
                        # Додаємо в початок черги, щоб "обмацувати" корабель відразу
                        self.target_queue.insert(0, (nr, nc))

        elif result == "SUNK":
            # Корабель знищено, очищуємо чергу цілей і повертаємось в Hunt
            self.target_queue = []


# --- ПРИКЛАД ІНТЕГРАЦІЇ В MAIN.PY ---
"""
В main.py тобі потрібно буде додати:
1. self.bot = BotStepashka()
2. У методі ходу бота:
   r, c = self.bot.get_shot_coordinates()
   res, sunk = player_board.receive_shot(r, c)
   self.bot.process_feedback(r, c, res if not sunk else "SUNK")
"""