# 🍣 UCUP-2026: Sushi Battle

> Класичний **Морський бій** у японсько-самурайському стилі, написаний на Python + Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## 📸 Скріншоти

| Меню | Розстановка | Бій |
|------|-------------|-----|
| Японські кораблі на хвилях | Розміщення суші-флоту | Двобій з ботом |

---

## 🎮 Про гру

Морський бій де замість кораблів — **суші-роли**, а поле бою оформлене у стилі японського живопису **Укіє-е** (Хокусай). Гравець бореться проти AI-бота «Stepashka», який використовує алгоритм **Hunt & Target**.

### Режими гри
- 🤖 **Гра з ботом** — проти AI Stepashka
- 👥 **Гра з другом** — hot-seat режим *(в розробці)*

---

## 🚀 Запуск

### 1. Встановіть Python 3.8+
Завантажте з [python.org](https://python.org). На Windows поставте галочку **"Add Python to PATH"**.

### 2. Встановіть Pygame

```bash
pip install pygame
```

### 3. Клонуйте або розпакуйте проект

```
sushi_battle/
├── main.py
├── menu.py
├── logic.py
├── ai.py
└── assets/
    ├── menu_bg.jpg
    ├── game_bg.jpg
    ├── board.jpg
    ├── roll.png
    ├── button_plate.png
    ├── button_plate_hover.png
    └── background_music.mp3
```

### 4. Запустіть

```bash
cd sushi_battle
python main.py
```

> **Без асетів теж працює!** Якщо папки `assets/` немає — гра запуститься з кольоровими замінниками замість графіки.

---

## 🕹️ Управління

| Дія | Клавіша / Кнопка |
|-----|-----------------|
| Розмістити корабель | ЛКМ по полю |
| Змінити напрямок (H/V) | **R** |
| Авторозстановка | Кнопка **AUTO-FILL** |
| Очистити поле | Кнопка **CLEAR ALL** |
| Почати бій | Кнопка **START BATTLE** |
| Зробити постріл | ЛКМ по полю бота |
| Вийти | Кнопка **ВИХІД** або закрити вікно |

---

## 🗂️ Структура коду

```
main.py   — Ігровий цикл, рендеринг, обробка подій (GameController)
logic.py  — Дані та правила гри (Board, Ship)
ai.py     — AI-бот Stepashka (Hunt & Target алгоритм)
menu.py   — Головне меню (Menu)
```

### Алгоритм бота (Hunt & Target)

```
HUNT mode  → стріляє випадково, не повторюючи клітинки
     ↓ влучання
TARGET mode → обстрілює сусідні клітинки навколо влучання
     ↓ потоплено
HUNT mode  → очищує чергу, повертається до пошуку
```

---

## ⚙️ Вимоги

- Python **3.8+**
- Pygame **2.x**
- ОС: Windows 10+, macOS 10.14+, Ubuntu 20.04+

---

## 📄 Ліцензія

MIT — використовуйте вільно.
