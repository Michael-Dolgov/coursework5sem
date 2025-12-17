from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QLabel, QTextEdit)
from controllers.image_controller import ImageController
from views.drop_area import DropArea
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обработка изображений")
        self.setMinimumSize(600, 600)
        
        self.controller = ImageController(self)
        
        self._setup_ui()
        
        self._connect_signals()
    
    def copy_to_clipboard(self, text_area, button):
        text = text_area.toPlainText()
        if text:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
            
            original_text = button.text()
            button.setText("✓ Скопировано!")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 5px;
                    min-height: 35px;
                }
            """)
        QTimer.singleShot(2000, lambda: self.reset_button(button, original_text))

    def reset_button(self, button, original_text):
        button.setText(original_text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
    
    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.drop_area = DropArea()
        layout.addWidget(self.drop_area)
        
        self.process_btn = QPushButton("Обработать")
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(self.process_btn)
        
        result_label = QLabel("Результат обработки:")
        result_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(result_label)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setPlaceholderText(
            "Здесь, будет отображена распознанная формула..."
        )
        self.result_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color:0
                background-color: #fafafa;
            }
        """)
        layout.addWidget(self.result_area, stretch=1)
        copy_btn = QPushButton("Копировать в буфер")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.result_area, copy_btn))
        layout.addWidget(copy_btn)
        
    def _connect_signals(self):
        """Подключение сигналов к слотам"""
        self.drop_area.image_dropped.connect(self.controller.on_image_loaded)
        self.process_btn.clicked.connect(self.controller.process_image)

