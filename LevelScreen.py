import os
import json
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QSizePolicy
from PyQt6.QtCore import Qt
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
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 30px;
            }
        """)

        # Загружаем лучшие результаты
        best_results = self.load_best_results()

        # Кнопки уровней - БЕЗ фиксированных размеров
        self.level3_btn = QPushButton(self.get_level_text(3, best_results))
        self.level4_btn = QPushButton(self.get_level_text(4, best_results))
        self.level5_btn = QPushButton(self.get_level_text(5, best_results))

        for btn in [self.level3_btn, self.level4_btn, self.level5_btn]:
            btn.setFont(QFont("Arial", 14))  # Увеличиваем шрифт
            # Устанавливаем размерную политику для растягивания
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumHeight(80)  # Только минимальная высота
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    border-radius: 15px;
                    padding: 20px;
                    color: black;
                    font-weight: bold;
                    margin: 5px 50px;  /* Отступы по бокам */
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
        buttons_container.setMaximumWidth(600)  # Максимальная ширина контейнера
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



