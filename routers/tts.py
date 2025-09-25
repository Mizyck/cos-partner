from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io
from services.tts_service import synthesize

router = APIRouter()

@router.post("/")
async def tts(text: str = Form(...), prompt_text: str = Form(""), prompt_audio: UploadFile = File(None)):
    prompt_bytes = await prompt_audio.read() if prompt_audio else None
    audio_bytes = synthesize(text = text, prompt_audio = prompt_bytes, prompt_text = prompt_text)
    return StreamingResponse(io.BytesIO(audio_bytes), medi_type = "audio/wav")