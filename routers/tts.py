from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os
from services.tts_service import synthesize

router = APIRouter()


@router.post("/")
async def tts(
    text: str = Form(..., description = "要合成的文本"),
    language: str = Form("zh"),
    prompt_audio: UploadFile = File(None, description = "参考音频")
):
    spk_path = None
    if prompt_audio:
        fd, spk_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        with open(spk_path, "wb") as f:
            f.write(await prompt_audio.read())

    out_path = synthesize(text=text, speaker_wav=spk_path, language=language)
    return FileResponse(out_path, media_type="audio/wav", filename="tts.wav")

    # 清理临时文件
    if spk_path and os.path.exists(spk_path):
        os.remove(spk_path)
        
