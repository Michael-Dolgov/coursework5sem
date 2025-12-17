import json
from PySide6.QtCore import QThread, Signal
import requests

class UploadThread(QThread):
    """Поток для отправки изображения на сервер"""
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, image_path: str, url: str):
        super().__init__()
        self.image_path = image_path
        self.url = url
    
    def run(self):
        try:
            with open(self.image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(self.url, files=files, timeout=30)
                response.raise_for_status()
                result = response.json()
                latex = result.get('latex', '')
                
                if not latex:
                    self.error.emit("Ошибка: сервер не вернул LaTeX код")
                    return
                self.finished.emit(str(latex))
        except requests.RequestException as e:
            self.error.emit(f"Ошибка сети: {str(e)}")
        except json.JSONDecodeError:
            self.error.emit("Ошибка: ответ не в формате JSON")
        except Exception as e:
            self.error.emit(f"Ошибка: {str(e)}")

