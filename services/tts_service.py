from pathlib import Path
import tempfile, os
import torch
import soundfile as sf
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

# 修补 torch.load 以支持加载完整模型（而不仅仅是权重）
_orig_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _orig_load(*args, **kwargs)
torch.load = _patched_load

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "XTTS-v2"

# 懒加载模型
_model = None
_config = None

# 加载模型
def get_model():
    global _model, _config
    if _model is None:
        # 加载配置
        _config = XttsConfig()
        _config.load_json(str(MODEL_DIR / "config.json"))

        # 初始化模型
        _model = Xtts.init_from_config(_config)
        _model.load_checkpoint(_config, checkpoint_dir=str(MODEL_DIR), eval=True)

        # 如果有 GPU 就放到 GPU
        if torch.cuda.is_available():
            _model.cuda()

    return _model, _config
    
# 语音克隆
def synthesize(text: str, speaker_wav: str = None, language: str = "zh") -> str:
    # 调用模型
    model, config = get_model()
    # 创建临时文件保存输出
    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    outputs = model.synthesize(
        text,
        config,
        speaker_wav=speaker_wav,
        gpt_cond_len=3,   # 上下文长度，可调
        language=language,
    )

    # 输出音频
    sf.write(out_path, outputs["wav"], config.audio.sample_rate)
    return out_path
