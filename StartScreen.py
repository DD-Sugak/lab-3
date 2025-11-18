from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSizePolicy, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from Background import BackgroundWidget

class StartScreen(BackgroundWidget):
    """Начальный экран с кнопкой 'Начать'"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Загрузка шрифта из файла
        font_id = QFontDatabase.addApplicationFont("Fronts/PressStart2P-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 24, QFont.Weight.Bold)
        else:
            custom_font = QFont("Arial", 24, QFont.Weight.Bold)

        title = QLabel("Игра в 15")
        title.setFont(custom_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #FF1493; 
                margin: 20px;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                padding: 20px;
            }
        """)

        start_btn = QPushButton("Начать игру")
        # Убираем фиксированные размеры
        start_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        start_btn.setMinimumHeight(100)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.9);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 24px;
                padding: 25px;
                margin: 0px 100px;  /* Отступы по бокам */
                min-height: 100px;
            }
            QPushButton:hover {
                background-color: rgba(188, 143, 143, 0.9);
            }
        """)

        # Контейнер для кнопки с ограничением ширины
        button_container = QWidget()
        button_container.setMaximumWidth(500)
        button_layout = QHBoxLayout(button_container)
        button_layout.addWidget(start_btn)

        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(50)
        layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)
        self.start_button = start_btn