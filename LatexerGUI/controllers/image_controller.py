import json
from typing import TYPE_CHECKING
from models.image_model import ImageModel
from models.upload_thread import UploadThread

if TYPE_CHECKING:
    from views.main_window import MainWindow


class ImageController:
    """Контроллер для управления обработкой изображений"""
    
    def __init__(self, view: 'MainWindow'):
        self.view = view
        self.model = ImageModel()
        self.upload_thread = None
    
    def on_image_loaded(self, path: str):
        """Обработка загрузки изображения"""
        if self.model.is_valid_image(path):
            self.model.image_path = path
            self.view.process_btn.setEnabled(True)
            self.view.result_area.clear()
            filename = self.model.get_filename()
            self.view.result_area.setPlaceholderText(
                f"Изображение загружено: {filename}"
            )
    
    def process_image(self):
        """Запуск обработки изображения"""
        if not self.model.image_path:
            return
        
        self._disable_processing()
        self.view.result_area.setText("Отправка изображения на сервер...")
        
        self.upload_thread = UploadThread(
            self.model.image_path, 
            self.model.api_url
        )
        self.upload_thread.finished.connect(self._on_process_finished)
        self.upload_thread.error.connect(self._on_process_error)
        self.upload_thread.start()
    
    def _on_process_finished(self, result: str):
        """Обработка успешного результата"""
        self.view.result_area.setPlainText(result)
        self._enable_processing()
    
    def _on_process_error(self, error_msg: str):
        """Обработка ошибки"""
        self.view.result_area.setText(f"{error_msg}")
        self._enable_processing()
    
    def _disable_processing(self):
        """Отключить возможность обработки"""
        self.view.process_btn.setEnabled(False)
        self.view.process_btn.setText("Обработка...")
    
    def _enable_processing(self):
        """Включить возможность обработки"""
        self.view.process_btn.setText("Обработать")
        self.view.process_btn.setEnabled(True)
