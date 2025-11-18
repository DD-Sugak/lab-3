from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Background import BackgroundWidget

class VictoryScreen(BackgroundWidget):
    """Экран победы"""

    def __init__(self, moves, time_elapsed, grid_size, parent=None):
        super().__init__(parent)
        self.moves = moves
        self.time_elapsed = time_elapsed
        self.grid_size = grid_size
        self.setup_ui()
        self.set_background("images/background.png")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Заголовок
        title = QLabel("ПОБЕДА!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #FFD700;
                margin: 20px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Статистика
        stats_layout = QVBoxLayout()

        time_label = QLabel(f"Время: {self.format_time(self.time_elapsed)}")
        moves_label = QLabel(f"Ходы: {self.moves}")
        level_label = QLabel(f"Уровень: {self.grid_size}x{self.grid_size}")

        for label in [time_label, moves_label, level_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                font-size: 18px; 
                margin: 5px;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 5px;
                padding: 5px;
            """)
            stats_layout.addWidget(label)

        # Кнопки
        buttons_layout = QHBoxLayout()

        play_again_btn = QPushButton("Играть снова")
        menu_btn = QPushButton("В меню")

        for btn in [play_again_btn, menu_btn]:
            btn.setMinimumSize(120, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 0.9);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 105, 180, 0.9);
                }
            """)
            buttons_layout.addWidget(btn)

        # Собираем все вместе
        layout.addWidget(title)
        layout.addLayout(stats_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Сохраняем ссылки на кнопки
        self.play_again_btn = play_again_btn
        self.menu_btn = menu_btn

    def format_time(self, seconds):
        """Форматирование времени"""
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}:{seconds:05.2f}"