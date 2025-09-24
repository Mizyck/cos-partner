from fastapi import APIRouter, UploadFile, File
import tempfile
from services.asr_service import transcribe_audio

router = APIRouter()

@router.post("/")
async def asr(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".wav") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        text, elapsed = transcribe_audio(tmp.name)
    return {"text": text, "status": "success", "latency_ms": int(elapsed * 1000)}
