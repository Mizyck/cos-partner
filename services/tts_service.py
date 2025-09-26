from TTS.api import TTS
import tempfile
import os

# 初始化模型
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

def synthesize(text: str, speaker_wav: str = None, language: str = "zh") -> str:
    # 生成临时文件保存音频
    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    # 文本转语音
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        file_path=out_path,
        language=language
    )
    return out_path
