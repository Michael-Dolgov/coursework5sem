from pathlib import Path
from typing import Optional


class ImageModel:
    """Модель для хранения данных изображения"""
    
    def __init__(self):
        self._image_path: Optional[str] = None
        self._api_url: str = "http://localhost:8000/tex/upload-image"
    
    @property
    def image_path(self) -> Optional[str]:
        return self._image_path
    
    @image_path.setter
    def image_path(self, path: str):
        self._image_path = path
    
    @property
    def api_url(self) -> str:
        return self._api_url
    
    @api_url.setter
    def api_url(self, url: str):
        self._api_url = url
    
    def is_valid_image(self, path: str) -> bool:
        """Проверка, является ли файл изображением"""
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        return path.lower().endswith(valid_extensions)
    
    def get_filename(self) -> str:
        """Получить имя файла изображения"""
        if self._image_path:
            return Path(self._image_path).name
        return ""
    
    def clear(self):
        """Очистить сохраненный путь"""
        self._image_path = None
