import os
import json
from PyQt6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QWidget,
                             QSizePolicy, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from Background import BackgroundWidget


class LevelScreen(BackgroundWidget):
    """Экран выбора уровня с лучшими результатами"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Выберите уровень сложности")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 30px;
                font-weight: bold;
            }
        """)

        # Загружаем лучшие результаты
        best_results = self.load_best_results()

        # Кнопки уровней
        self.level3_btn = QPushButton(self.get_level_text(3, best_results))
        self.level4_btn = QPushButton(self.get_level_text(4, best_results))
        self.level5_btn = QPushButton(self.get_level_text(5, best_results))

        for btn in [self.level3_btn, self.level4_btn, self.level5_btn]:
            btn.setFont(QFont("Arial", 14))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumHeight(80)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    border-radius: 15px;
                    padding: 20px;
                    color: black;
                    font-weight: bold;
                    margin: 5px 50px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.8);
                    color: #FFD700;
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 0.5);
                    border: 2px solid #FFD700;
                    color: #FFD700;
                }
            """)

        # Контейнер для кнопок с ограничением максимальной ширины
        buttons_container = QWidget()
        buttons_container.setMaximumWidth(600)
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)

        buttons_layout.addWidget(self.level3_btn)
        buttons_layout.addWidget(self.level4_btn)
        buttons_layout.addWidget(self.level5_btn)

        # Основной layout
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

        self.buttons = {
            3: self.level3_btn,
            4: self.level4_btn,
            5: self.level5_btn
        }

        # Создаём Overlay для загрузки
        self.create_loading_overlay()

    def create_loading_overlay(self):
        """Создает overlay для загрузки с абсолютным позиционированием"""
        # Overlay затемняет весь экран
        self.loading_overlay = QWidget(self)
        self.loading_overlay.setStyleSheet("background: rgba(0, 0, 0, 0.7);")
        self.loading_overlay.hide()

        # Текст загрузки БЕЗ фона
        self.loading_label = QLabel("Загрузка...", self.loading_overlay)
        self.loading_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                padding: 20px;
            }
        """)
        self.loading_label.setMinimumSize(400, 100)

    def load_best_results(self):
        """Загружает лучшие результаты из файла"""
        try:
            if os.path.exists('best_results.json'):
                with open('best_results.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def get_level_text(self, level, best_results):
        """Формирует текст для кнопки уровня"""
        level_key = str(level)
        if level_key in best_results:
            result = best_results[level_key]
            time_str = self.format_time(result['time'])
            return f"{level}x{level}\nЛучший: {result['moves']} ходов, {time_str}"
        else:
            return f"{level}x{level}\nЛучший: ---"

    def format_time(self, seconds):
        """Форматирование времени"""
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}:{seconds:05.2f}"

    def update_results(self):
        """Обновляет отображение лучших результатов"""
        best_results = self.load_best_results()

        self.level3_btn.setText(self.get_level_text(3, best_results))
        self.level4_btn.setText(self.get_level_text(4, best_results))
        self.level5_btn.setText(self.get_level_text(5, best_results))

    def show_loading(self, level):
        """Показывает индикатор загрузки"""
        # Отключаем все кнопки
        for btn in self.buttons.values():
            btn.setEnabled(False)

        # Устанавливаем текст
        self.loading_label.setText(f"Загрузка уровня\n{level}x{level}...")

        # Показываем overlay на весь экран
        self.loading_overlay.resize(self.size())
        self.loading_overlay.show()

        # Центрируем текст
        self.loading_label.move(
            (self.width() - self.loading_label.width()) // 2,
            (self.height() - self.loading_label.height()) // 2
        )

    def hide_loading(self):
        """Скрывает индикатор загрузки и включает кнопки"""
        self.loading_overlay.hide()
        for btn in self.buttons.values():
            btn.setEnabled(True)

    def resizeEvent(self, event):
        """При изменении размера окна обновляем позиции"""
        super().resizeEvent(event)
        if self.loading_overlay.isVisible():
            self.loading_overlay.resize(self.size())
            self.loading_label.move(
                (self.width() - self.loading_label.width()) // 2,
                (self.height() - self.loading_label.height()) // 2
            )