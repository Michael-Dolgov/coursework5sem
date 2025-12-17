import os
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse

from services.tex_service import TexRecognitionService
from modules.TexTeller.texteller import get_tex_model

router = APIRouter(prefix="/tex")

def get_tex_service():
    return TexRecognitionService(get_tex_model())

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    service: TexRecognitionService = Depends(get_tex_service)
):

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
        return JSONResponse(
            status_code=400,
            content={"error": "Файл должен быть изображением"}
        )

    image_bytes = await file.read()
    save_path = f"images/{file.filename}"

    with open(save_path, "wb") as f:
        f.write(image_bytes)

    latex = service.recognize(save_path)

    os.remove(save_path)

    return {
        "filename": file.filename,
        "latex": latex
    }

