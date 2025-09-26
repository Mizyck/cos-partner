from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import FileResponse
import tempfile
import os
from services.tts_service import synthesize

router = APIRouter()


@router.post("/")
async def tts(
    text: str = Form(...),
    language: str = Form("zh"),
    prompt_audio: UploadFile = None
):
    spk_path = None
    if prompt_audio:
        fd, spk_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        with open(spk_path, "wb") as f:
            f.write(await prompt_audio.read())

    out_path = synthesize(text=text, speaker_wav=spk_path, language=language)
    return FileResponse(out_path, media_type="audio/wav", filename="tts.wav")
