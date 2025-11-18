import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QStackedWidget, QGridLayout, QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap
import random


class StartScreen(QWidget):
    """Начальный экран с кнопкой 'Начать'"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Загрузка шрифта из файла
        font_id = QFontDatabase.addApplicationFont("Fronts/PressStart2P-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 24, QFont.Weight.Bold)
        else:
            # Если шрифт не загрузился, используем fallback
            custom_font = QFont("Arial", 24, QFont.Weight.Bold)
            print("Не удалось загрузить пользовательский шрифт")
        # Заголовок
        title = QLabel("Игра в 15")
        title.setFont(custom_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FF1493; margin: 20px;")

        # Кнопка начать
        start_btn = QPushButton("Начать игру")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 20px;
                min-width: 150px;    
                max-width: 150px;   
                min-height: 80px;    
                max-height: 80px;
                margin: 0px 50px;
            }
            QPushButton:hover {
                background-color: #BC8F8F;
            }
        """)
        layout.addStretch()  # Растягиваемое пространство СВЕРХУ
        layout.addWidget(title)  # Заголовок
        layout.addSpacing(40)  # Отступ между заголовком и кнопкой
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)  # Кнопка по центру
        layout.addStretch()

        self.setLayout(layout)

        # Сохраняем ссылку на кнопку для подключения сигналов
        self.start_button = start_btn


class LevelScreen(QWidget):
    """Экран выбора уровня"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Выберите уровень сложности")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопки уровней
        level3_btn = QPushButton("3x3")
        level4_btn = QPushButton("4x4")
        level5_btn = QPushButton("5x5")

        # Настройка кнопок
        for btn in [level3_btn, level4_btn, level5_btn]:
            btn.setFont(QFont("Arial", 12))
            btn.setMinimumHeight(40)

        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(level3_btn)
        layout.addWidget(level4_btn)
        layout.addWidget(level5_btn)
        layout.addStretch()

        self.setLayout(layout)

        # Сохраняем ссылки на кнопки
        self.buttons = {
            3: level3_btn,
            4: level4_btn,
            5: level5_btn
        }


class GameScreen(QWidget):
    """Базовый игровой экран"""

    def __init__(self, grid_size, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.tiles = []
        self.board = []
        self.empty_pos = (grid_size - 1, grid_size - 1)
        self.moves = 0

        self.image_path = os.path.abspath('images/1.png')
        self.has_custom_image = os.path.exists(self.image_path)

        self.setup_ui()
        self.init_game()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Отступы только от краев окна

        # Заголовок с информацией
        info_layout = QHBoxLayout()

        self.moves_label = QLabel(f"Ходы: {self.moves}")
        self.moves_label.setFont(QFont("Arial", 12))

        back_btn = QPushButton("← Назад")
        back_btn.setFont(QFont("Arial", 10))
        back_btn.clicked.connect(self.go_back)

        info_layout.addWidget(back_btn)
        info_layout.addStretch()
        info_layout.addWidget(self.moves_label)

        # Игровое поле
        self.board_widget = QWidget()
        self.grid_layout = QGridLayout(self.board_widget)

        # ⭐ ВАЖНО: УБИРАЕМ ВСЕ ОТСТУПЫ ⭐
        self.grid_layout.setSpacing(0)  # НУЛЕВОЕ расстояние между клетками
        self.grid_layout.setContentsMargins(0, 0, 0, 0)  # НУЛЕВЫЕ внешние отступы
        self.grid_layout.setHorizontalSpacing(0)  # НУЛЬ между колонками
        self.grid_layout.setVerticalSpacing(0)  # НУЛЬ между строками

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
        """Создает клетки БЕЗ расстояний между ними"""
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = QPushButton("")

                # Размер клеток
                if self.grid_size == 3:
                    btn_size = 150
                    font_size = 18
                elif self.grid_size == 4:
                    btn_size = 110
                    font_size = 16
                else:  # 5x5
                    btn_size = 90
                    font_size = 14

                btn.setFixedSize(btn_size, btn_size)
                btn.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
                btn.clicked.connect(lambda checked, x=i, y=j: self.tile_clicked(x, y))

                # ⭐ Убираем все отступы у кнопки ⭐
                btn.setStyleSheet("""
                    QPushButton {
                        margin: 0px;
                        padding: 0px;
                        border: none;
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
        self.update_display()
        self.shuffle_board()

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

        self.moves = 0
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
                self.show_win_message()

    def update_display(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                btn = self.tiles[i][j]

                if value == 0:
                    btn.setText("")
                    btn.setIcon(QIcon())
                    btn.setStyleSheet("""
                           QPushButton {
                               background-color: #f0f0f0;
                               border: 1px solid #d0d0d0;
                               margin: 0px;
                               padding: 0px;
                           }
                       """)
                    btn.setEnabled(False)

                elif value == 1 and self.has_custom_image:
                    btn.setText("")
                    btn.setIcon(QIcon(self.image_path))
                    btn.setIconSize(btn.size())
                    btn.setStyleSheet(f"""
                            QPushButton {{
                                background-color: #87CEEB;
                                border: 2px solid #4682B4;
                                border-radius: 15px;
                                margin: 0px;
                                padding: 0px;
                            }}
                        """)
                    btn.setEnabled(True)
                else:
                    # Обычные цифры
                    btn.setText(str(value))
                    btn.setIcon(QIcon())
                    btn.setStyleSheet("""
                           QPushButton {
                               background-color: #87CEEB;
                               border: 1px solid #4682B4;
                               margin: 0px;
                               padding: 0px;
                               font-weight: bold;
                               color: black;
                           }
                           QPushButton:hover {
                               background-color: #6495ED;
                           }
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

    def show_win_message(self):
        """Показывает сообщение о победе"""
        msg = QMessageBox()
        msg.setWindowTitle("Победа!")
        msg.setText(f"Поздравляем! Вы выиграли!\nХодов: {self.moves}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def go_back(self):
        """Возврат к выбору уровня"""
        parent = self.parent()
        while parent and not isinstance(parent, QStackedWidget):
            parent = parent.parent()
        if parent:
            parent.setCurrentIndex(1)


class Game15(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра в 15")
        self.setFixedSize(700, 700)  # Фиксированный размер

        self.setup_ui()

    def setup_ui(self):
        # Создаем stacked widget для переключения между экранами
        self.stacked_widget = QStackedWidget()

        # Создаем экраны
        self.start_screen = StartScreen()
        self.level_screen = LevelScreen()

        # Добавляем экраны в stacked widget
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.level_screen)

        self.setCentralWidget(self.stacked_widget)

        # Подключаем сигналы
        self.connect_signals()

    def connect_signals(self):
        # Подключение кнопки "Начать" на начальном экране
        self.start_screen.start_button.clicked.connect(self.show_level_screen)

        # Подключение кнопок выбора уровня
        for size, button in self.level_screen.buttons.items():
            button.clicked.connect(lambda checked, s=size: self.start_game(s))

    def show_level_screen(self):
        """Показать экран выбора уровня"""
        self.stacked_widget.setCurrentIndex(1)

    def start_game(self, grid_size):
        """Запуск игры с выбранным размером поля"""
        # Создаем игровой экран
        game_screen = GameScreen(grid_size)

        # Добавляем в stacked widget
        self.stacked_widget.addWidget(game_screen)
        self.stacked_widget.setCurrentWidget(game_screen)


def main():
    app = QApplication(sys.argv)
    window = Game15()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()