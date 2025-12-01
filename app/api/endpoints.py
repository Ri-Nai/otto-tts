from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.tts import TTSRequest
from app.core.tts_engine import TTSEngine
import io
import soundfile as sf
import httpx

router = APIRouter()

# Initialize the engine. 
# Note: This assumes the application is run from the project root.
try:
    tts_engine = TTSEngine()
except Exception as e:
    print(f"Failed to initialize TTS Engine: {e}")
    tts_engine = None

def _generate_response(request: TTSRequest):
    if tts_engine is None:
        raise HTTPException(status_code=500, detail="TTS Engine not initialized")
        
    try:
        audio_data, sample_rate = tts_engine.generate_audio_data(
            request.text,
            request.inYsddMode,
            request.pitchMult,
            request.speedMult,
            request.norm,
            request.reverse
        )
        
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sample_rate, format='WAV')
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/otto")
async def generate_audio(request: TTSRequest):
    return _generate_response(request)

@router.get("/generate/otto")
async def generate_audio_get(
    text: str,
    inYsddMode: bool = True,
    pitchMult: float = 1.0,
    speedMult: float = 1.0,
    norm: bool = False,
    reverse: bool = False
):
    request = TTSRequest(
        text=text,
        inYsddMode=inYsddMode,
        pitchMult=pitchMult,
        speedMult=speedMult,
        norm=norm,
        reverse=reverse
    )
    return _generate_response(request)

@router.get("/generate/manbo")
async def tts_proxy(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")

    target_api = "https://api.milorapart.top/apis/mbAIsc"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Call third-party API
            resp = await client.get(target_api, params={"text": text})
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") != 200 or not data.get("url"):
                raise HTTPException(status_code=502, detail=f"Upstream API error: {data}")
                
            audio_url = data["url"]
            
            # 2. Download audio file
            audio_resp = await client.get(audio_url)
            audio_resp.raise_for_status()
            audio_content = audio_resp.content
            
            # 3. Return audio stream
            return StreamingResponse(io.BytesIO(audio_content), media_type="audio/mpeg")
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Upstream API connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
