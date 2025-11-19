import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget)
from PyQt6.QtCore import  QTimer

from GameScreen import GameScreen
from StartScreen import StartScreen
from LevelScreen import LevelScreen


class Game15(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра в 15")
        self.setMinimumSize(700, 700)
        self.background_image = "images/background.png"
        self.setup_ui()
        self.set_background()

    def setup_ui(self):
        self.stacked_widget = QStackedWidget()

        self.start_screen = StartScreen()
        self.level_screen = LevelScreen()

        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.level_screen)

        self.setCentralWidget(self.stacked_widget)
        self.connect_signals()

    def set_background(self):
        """Устанавливает фоновое изображение для всех экранов"""
        if os.path.exists(self.background_image):
            # Устанавливаем фон для всех экранов
            self.start_screen.set_background(self.background_image)
            self.level_screen.set_background(self.background_image)
        else:
            print(f"Фоновое изображение не найдено: {self.background_image}")

    def connect_signals(self):

        self.start_screen.start_button.clicked.connect(self.show_level_screen)

        for size, button in self.level_screen.buttons.items():
            button.clicked.connect(lambda checked, s=size: self.start_game(s))

    def show_level_screen(self):
        """Показать экран выбора уровня"""
        # Обновляем результаты на экране выбора уровня
        self.level_screen.update_results()
        self.stacked_widget.setCurrentIndex(1)

    def update_level_screen(self):
        """Обновляет экран выбора уровня"""
        self.level_screen.update_results()

    def start_game(self, grid_size):
        """Запуск игры с выбранным размером поля"""
        # Показываем индикатор загрузки
        self.level_screen.show_loading(grid_size)

        # Запускаем игру с небольшой задержкой
        QTimer.singleShot(100, lambda: self.create_game_screen(grid_size))


    def create_game_screen(self, grid_size):
        """Создает и показывает игровой экран"""
        game_screen = GameScreen(grid_size)
        self.stacked_widget.addWidget(game_screen)
        self.stacked_widget.setCurrentWidget(game_screen)

        # Устанавливаем фон для игрового экрана
        game_screen.set_background(self.background_image)

        # Скрываем индикатор загрузки
        self.level_screen.hide_loading()


def main():
    app = QApplication(sys.argv)
    window = Game15()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()