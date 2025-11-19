from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from Background import BackgroundWidget

class StartScreen(BackgroundWidget):
    """Начальный экран с кнопкой 'Начать'"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Основной layout - вертикальный
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        layout.setContentsMargins(50, 50, 50, 50)  # Отступы от краев

        # Заголовок
        title = QLabel("Игра в 15")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #FF1493;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
            }
        """)

        # Кнопка
        start_btn = QPushButton("Начать игру")
        start_btn.setMinimumSize(400, 100)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.9);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: rgba(188, 143, 143, 0.9);
            }
        """)

        # Компоновка
        layout.addStretch()  # Растягивающее пространство сверху
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)  # Отступ между заголовком и кнопкой
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()  # Растягивающее пространство снизу

        self.setLayout(layout)
        self.start_button = start_btn