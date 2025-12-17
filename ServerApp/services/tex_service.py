class TexRecognitionService:
    def __init__(self, model):
        self.model = model
    
    def recognize(self, filepath: str) -> str:
        return self.model.recognize(filepath)
