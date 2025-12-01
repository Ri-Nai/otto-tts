from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Otto TTS API", description="电棍活字印刷术 TTS API")

app.include_router(endpoints.router, prefix="/api/v1", tags=["tts"])

@app.get("/")
async def root():
    return {"message": "Welcome to Otto TTS API"}
