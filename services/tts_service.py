import os
import sys
import io
import tempfile
import wave
from typing import Optional

import torch
import torchaudio

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 拼接 CosyVoice 的路径（相对项目根目录）
COSYVOICE_PATH = os.path.join(BASE_DIR, "CosyVoice")

# 加入 sys.path
if COSYVOICE_PATH not in sys.path:
    sys.path.append(COSYVOICE_PATH)

# 懒加载模型
_cosy = None
_SAMPLE_RATE = 16000


# 确保模型目录存在
def _ensure_dir(path: str):
    os.makedirs(path, exist_ok = True)

# 加载参照音频
def _load_prompt_wav(prompt_bytes: bytes, sample_rate:int = _SAMPLE_RATE):
    with tempfile.NamedTemporaryFile(suffix = ".wav", delete = True) as tmp:
        tmp.write(prompt_bytes)
        tmp.flush()
        wav, sr = torchaudio.load(tmp.name)
        if sr != sample_rate:
            wav = torchaudio.functional.resample(wav, sr, sample_rate)
        if wav.shape[0] > 1:
            wav = wav.mean(dim = 0, keepdim = True)
        return wav.squeeze(0), sample_rate
    
# 读取模型生成的wavform(Tensor)， 保存到内存缓冲区（BytesIO），格式为wav，输出wav格式字节流
def _save_wav_bytes(waveform: torch.Tensor, sample_rate: int) -> bytes:
    buf = io.BytesIO()
    torchaudio.save(buf, waveform.unsqueeze(0), sample_rate, format = "wav")
    buf.seek(0)
    return buf.read()

# 加载模型
def get_cosyvoive(model_root = "./models/tts/CosyVoice2-0.5B", fp16 = True):
    global _cosy
    # 如果模型已经加载过则直接返回
    if _cosy is not None:
        return _cosy

    _ensure_dir(model_root)     # 确保模型目录存在
    # 如果目录为空则调用 modelscope.snapshot_download 下载模型到本地 ./models/tts/
    if not os.path.exists(model_root) or not os.listdir(model_root):
        from modelscope import snapshot_download
        os.environ["MODELSCOPE_CACHE"] = model_root
        snapshot_download('iic/CosyVoice2-0.5B', local_dir = model_root)
    
    # 导入CosyVoice2 模型，支持 fp16
    from cosyvoice.cli.cosyvoice import CosyVoice2
    _cosy = CosyVoice2(model_root, fp16 = fp16)
    return _cosy    # 返回模型实例

# 语音合成
# text: 要合成的文本
# prompt_audio: 可选的参考音频（二进制）， 用于zero-shot语音克隆
# prompt_text： 可选的参考文本
def synthesize(text: str, prompt_audio: Optional[bytes] = None, prompt_text: str = "") -> bytes:
    cosy = get_cosyvoive()
    # 有参考音频
    if prompt_audio:
        prompt_wav, _ = _load_prompt_wav(prompt_audio)
        chunks = list(cosy.inference_zero_shot(text, prompt_text, prompt_wav.numpy()))
    # 无参考音频
    else:
        chunks = list(cosy.inference_zero_shot(text, "", None))
    # cosyvoice返回分块结果，提取其中的tts_speech
    waves = [c['tts_speech'] for c in chunks if 'tts_speech' in c]
    
    # 异常处理
    if not waves:
        raise RuntimeError("未生成音频")
    # 拼接所有chunk
    waveform = torch.cat(waves, dim = -1)
    return _save_wav_bytes(waveform, cosy.sample_rate)

    


