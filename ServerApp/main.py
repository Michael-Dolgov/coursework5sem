from fastapi import FastAPI
from routes.tex_recognition import router as tex_router
import uvicorn

app = FastAPI(
    title="Tex Recognition API",
    description="API для распознавания формул через TexTellerModel",
    version="1.0.0"
)
app.include_router(tex_router)

@app.on_event("startup")
async def startup_event():
    app.state.tex_model = None

@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}

def main():

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
