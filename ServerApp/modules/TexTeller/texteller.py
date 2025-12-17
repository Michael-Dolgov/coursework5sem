# modules/texteller_model.py
import re
from texteller import load_model, load_tokenizer, img2latex

_tex_model_singleton = None

class TexTellerModel:
    def __init__(self):
        self.model = load_model(use_onnx=False)
        self.tokenizer = load_tokenizer()
     
    def recognize(self, filepath: str):
        recognized_raw = img2latex(
            self.model, 
            self.tokenizer, 
            [filepath]
        )
        recognized_latex = recognized_raw[0]
        recognized_one_line = re.sub(r"\s+", " ", recognized_latex).strip()
        return recognized_one_line

def get_tex_model() -> TexTellerModel:
    global _tex_model_singleton

    if _tex_model_singleton is None:
        _tex_model_singleton = TexTellerModel()

    return _tex_model_singleton
