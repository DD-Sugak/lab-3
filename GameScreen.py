import os
import json
import random
from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QGridLayout, QSizePolicy, QStackedWidget, QMainWindow)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

from Background import BackgroundWidget
from VictoryScreen import VictoryScreen

class GameScreen(BackgroundWidget):
    """Базовый игровой экран"""

    def __init__(self, grid_size, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.tiles = []
        self.board = []
        self.empty_pos = (grid_size - 1, grid_size - 1)
        self.moves = 0
        self.elapsed_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        # ПРЕДЗАГРУЗКА КАРТИНОК В ПАМЯТЬ
        self.tile_icons = {}
        self.tile_pixmaps = {}
        self.preload_tile_images()

        self.setup_ui()
        self.init_game()

    def preload_tile_images(self):
        """Предзагружает все картинки в память"""
        for i in range(1, 25):
            image_path = f"images/{i}.png"
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.tile_pixmaps[i] = pixmap
                self.tile_icons[i] = QIcon(pixmap)
            else:
                print(f"Изображение не найдено: {image_path}")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Уменьшили отступы

        # Заголовок с информацией
        info_layout = QHBoxLayout()

        self.time_label = QLabel("Время: 0:00.00")
        self.time_label.setFont(QFont("Arial", 18))
        self.time_label.setStyleSheet("background: rgba(255, 255, 255, 0.7); padding: 3px; border-radius: 3px;")

        self.moves_label = QLabel(f"Ходы: {self.moves}")
        self.moves_label.setFont(QFont("Arial", 18))
        self.moves_label.setStyleSheet("background: rgba(255, 255, 255, 0.7); padding: 3px; border-radius: 3px;")

        back_btn = QPushButton("← Назад")
        back_btn.setFont(QFont("Arial", 18))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 5px;
                padding: 5px 10px;
                color: black;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.8);
                color: #FFD700;
            }
        """)
        back_btn.clicked.connect(self.go_back)

        info_layout.addWidget(back_btn)
        info_layout.addStretch()
        info_layout.addWidget(self.time_label)
        info_layout.addSpacing(10)
        info_layout.addWidget(self.moves_label)

        # Игровое поле
        self.board_widget = QWidget()
        self.board_widget.setStyleSheet("background: rgba(255, 255, 255, 0.1); border-radius: 5px; padding: 5px;")
        self.grid_layout = QGridLayout(self.board_widget)
        self.grid_layout.setSpacing(1)  # Уменьшили расстояние между клетками
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Создаем клетки
        self.create_tiles()
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.board_widget)
        center_layout.addStretch()

        # Собираем все вместе
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def create_tiles(self):
        """Создает клетки """
        # размеры для разных уровней
        size_config = {
            3: {'btn_size': 150, 'font_size': 16},
            4: {'btn_size': 120, 'font_size': 14},
            5: {'btn_size': 120, 'font_size': 12}
        }
        config = size_config.get(self.grid_size, {'btn_size': 90, 'font_size': 14})

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = QPushButton()
                btn.setFixedSize(config['btn_size'], config['btn_size'])
                btn.setFont(QFont("Arial", config['font_size'], QFont.Weight.Bold))
                btn.clicked.connect(lambda checked, x=i, y=j: self.tile_clicked(x, y))

                # Минималистичный стиль
                btn.setStyleSheet("""
                    QPushButton {
                        margin: 0px;
                        padding: 0px;
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        background-color: rgba(255, 255, 255, 0.1);
                    }
                    QPushButton:hover {
                        border: 2px solid #FFD700;
                    }
                """)

                self.grid_layout.addWidget(btn, i, j)
                row.append(btn)
            self.tiles.append(row)

    def init_game(self):
        """Инициализация игрового поля"""
        self.board = []
        counter = 1
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                if counter < self.grid_size * self.grid_size:
                    row.append(counter)
                else:
                    row.append(0)
                counter += 1
            self.board.append(row)

        self.empty_pos = (self.grid_size - 1, self.grid_size - 1)
        self.moves = 0
        self.elapsed_time = 0
        self.update_display()
        self.shuffle_board()

        # Запускаем таймер
        self.timer.start(100)  # Обновление каждые 100 мс

    def update_time(self):
        """Обновление времени"""
        self.elapsed_time += 0.1
        self.time_label.setText(f"Время: {self.format_time(self.elapsed_time)}")

    def format_time(self, seconds):
        """Форматирование времени"""
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}:{seconds:05.2f}"

    def shuffle_board(self):
        """Перемешивает поле"""
        for _ in range(100 * self.grid_size):
            i, j = self.empty_pos
            possible_moves = []

            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                    possible_moves.append((ni, nj))

            if possible_moves:
                move_i, move_j = random.choice(possible_moves)
                self.board[i][j], self.board[move_i][move_j] = \
                    self.board[move_i][move_j], self.board[i][j]
                self.empty_pos = (move_i, move_j)

        self.update_display()

    def tile_clicked(self, i, j):
        """Обработка клика по клетке"""
        empty_i, empty_j = self.empty_pos

        if ((abs(i - empty_i) == 1 and j == empty_j) or
                (abs(j - empty_j) == 1 and i == empty_i)):

            self.board[empty_i][empty_j] = self.board[i][j]
            self.board[i][j] = 0
            self.empty_pos = (i, j)

            self.moves += 1
            self.update_display()

            if self.check_win():
                QTimer.singleShot(200, self.show_victory_screen)

    def update_display(self):
        """Оптимизированное обновление отображения"""
        self.moves_label.setText(f"Ходы: {self.moves}")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                btn = self.tiles[i][j]

                if value == 0:
                    # Пустая клетка
                    btn.setText("")
                    btn.setIcon(QIcon())
                    btn.setStyleSheet("background-color: transparent; border: 1px solid rgba(255,255,255,0.1);")
                    btn.setEnabled(False)
                else:
                    # Используем предзагруженные иконки
                    if value in self.tile_icons:
                        btn.setIcon(self.tile_icons[value])
                        btn.setIconSize(btn.size())
                        btn.setText("")
                        btn.setStyleSheet(
                            "background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.3);")
                    else:
                        # Fallback на цифры
                        btn.setText(str(value))
                        btn.setIcon(QIcon())
                        btn.setStyleSheet("""
                             background-color: rgba(135,206,235,0.8); 
                             border: 1px solid #4682B4; 
                             color: black; 
                             font-weight: bold;
                         """)
                    btn.setEnabled(True)


    def check_win(self):
        """Проверяет, выиграл ли игрок"""
        counter = 1
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i == self.grid_size - 1 and j == self.grid_size - 1:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != counter:
                        return False
                    counter += 1
        return True

    def show_victory_screen(self):
        """Показывает экран победы"""
        self.timer.stop()

        # Сохраняем результат
        self.save_best_result()

        victory_screen = VictoryScreen(self.moves, self.elapsed_time, self.grid_size)

        parent = self.parent()
        while parent and not isinstance(parent, QStackedWidget):
            parent = parent.parent()

        if parent:
            parent.addWidget(victory_screen)
            parent.setCurrentWidget(victory_screen)

            # ТОЛЬКО подключение кнопки "В меню"
            victory_screen.menu_btn.clicked.connect(lambda: self.go_to_menu(parent))

    def save_best_result(self):
        """Сохраняет лучший результат"""
        try:
            # Пытаемся загрузить существующие результаты
            if os.path.exists('best_results.json'):
                with open('best_results.json', 'r') as f:
                    best_results = json.load(f)
            else:
                best_results = {}

            level_key = str(self.grid_size)

            # Проверяем, является ли текущий результат лучшим
            if level_key not in best_results:
                best_results[level_key] = {
                    'moves': self.moves,
                    'time': self.elapsed_time
                }
            else:
                current_best = best_results[level_key]
                # Считаем лучшим результат с меньшим количеством ходов
                if self.moves < current_best['moves']:
                    best_results[level_key] = {
                        'moves': self.moves,
                        'time': self.elapsed_time
                    }
                # При одинаковых ходах - лучшее время
                elif self.moves == current_best['moves'] and self.elapsed_time < current_best['time']:
                    best_results[level_key] = {
                        'moves': self.moves,
                        'time': self.elapsed_time
                    }

            # Сохраняем результаты
            with open('best_results.json', 'w') as f:
                json.dump(best_results, f)

        except Exception as e:
            print(f"Ошибка при сохранении результатов: {e}")




    def go_to_menu(self, stacked_widget):
        """Возврат в главное меню"""
        self.timer.stop()
        stacked_widget.setCurrentIndex(1)
        stacked_widget.removeWidget(self)

    def go_back(self):
        """Возврат к выбору уровня"""
        self.timer.stop()

        parent = self.parent()
        while parent and not isinstance(parent, QStackedWidget):
            parent = parent.parent()
        if parent:
            parent.setCurrentIndex(1)
            parent.removeWidget(self)
