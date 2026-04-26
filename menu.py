import pygame


class Menu:
    def __init__(self, screen, font, assets=None):
        self.screen = screen
        self.font = font

        # Налаштування розмірів (під твій дизайн)
        self.button_width = 380
        self.button_height = 85
        self.center_x = screen.get_width() // 2 - self.button_width // 2

        # Завантаження графіки
        self.bg = self._load_asset("assets/menu_bg.jpg", (screen.get_width(), screen.get_height()), False)
        self.btn_img = self._load_asset("assets/button_plate.png", (self.button_width, self.button_height), True)
        self.btn_hover = self._load_asset("assets/button_plate_hover.png", (self.button_width, self.button_height),
                                          True)

    def _load_asset(self, path, size, alpha):
        """Допоміжна функція для безпечного завантаження фото"""
        try:
            img = pygame.image.load(path)
            img = img.convert_alpha() if alpha else img.convert()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Не вдалося завантажити {path}: {e}")
            return None

    def draw_button(self, text, y_pos):
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(self.center_x, y_pos, self.button_width, self.button_height)
        is_hovered = rect.collidepoint(mouse_pos)

        # 1. Малюємо графічну підкладку (кнопку)
        if is_hovered and self.btn_hover:
            self.screen.blit(self.btn_hover, rect)
        elif self.btn_img:
            self.screen.blit(self.btn_img, rect)
        else:
            # Якщо фото немає — малюємо солідний коричневий прямокутник
            color = (160, 82, 45) if is_hovered else (139, 69, 19)
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=12)

        # 2. Малюємо текст із тінню
        # Тінь (темно-коричнева)
        shadow_surf = self.font.render(text, True, (40, 20, 0))
        # Основний текст (світлий крем/білий)
        text_surf = self.font.render(text, True, (250, 245, 230))

        # Центруємо через Rect (це найнадійніший спосіб)
        text_rect = text_surf.get_rect(center=rect.center)

        # Блітінг: спочатку тінь (зі зміщенням), потім текст
        self.screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surf, text_rect)

        return rect

    def draw(self):
        # 1. Фон
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((44, 62, 80))  # Темно-синій океан як запасний фон

        # 2. Кнопки (вирівняні по вертикалі)
        # Повертаємо їх, щоб у main.py можна було перевірити collidepoint
        btn_ai = self.draw_button("ГРА З БОТОМ", 230)
        btn_friend = self.draw_button("ГРА З ДРУГОМ", 330)
        btn_exit = self.draw_button("ВИХІД", 430)

        return btn_ai, btn_friend, btn_exit