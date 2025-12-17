from PySide6.QtWidgets import QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent


class DropArea(QLabel):
    """Область для перетаскивания изображений"""
    image_dropped = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Перетащите изображение сюда\nили нажмите для выбора")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
                padding: 20px;
                font-size: 14px;
                color: #666;
                min-height: 200px;
            }
            QLabel:hover {
                border-color: #666;
                background-color: #e8e8e8;
            }
        """)
        self.image_path = None
        self.setMinimumHeight(250)
        
        # Кнопка закрытия (крестик)
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.7);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(200, 0, 0, 1);
            }
        """)
        self.close_btn.clicked.connect(self.clear_image)
        self.close_btn.hide()  # Скрыта по умолчанию
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.set_image(file_path)
                self.image_dropped.emit(file_path)
    
    def set_image(self, path: str):
        """Установить и отобразить изображение"""
        self.image_path = path
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(400, 200, Qt.KeepAspectRatio, 
                                         Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
            self.setText("")
            self.close_btn.show()  # Показать кнопку закрытия
            self._update_close_button_position()
    
    def clear_image(self):
        """Очистить отображаемое изображение"""
        self.clear()
        self.image_path = None
        self.setText("Перетащите изображение сюда\nили нажмите для выбора")
        self.close_btn.hide()  # Скрыть кнопку закрытия
    
    def resizeEvent(self, event):
        """Обновить позицию кнопки при изменении размера"""
        super().resizeEvent(event)
        if self.image_path:
            self._update_close_button_position()
    
    def _update_close_button_position(self):
        """Расположить кнопку в правом верхнем углу"""
        self.close_btn.move(self.width() - self.close_btn.width() - 10, 10)