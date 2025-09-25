from funasr import AutoModel
import time
import os


# 指定模型缓存路径（models/asr）
model_dir = os.path.join(os.getcwd(), "models", "asr")
os.makedirs(model_dir, exist_ok = True)

_asr_model = None # 全局变量，懒加载

def get_asr_model():
    global _asr_model
    if _asr_model is None:
        _asr_model = AutoModel(
            model = "paraformer-zh", 
            vad_model = "fsmn-vad", 
            punc_model = "ct-punc",
            cache_dir = model_dir,  # 指定模型缓存路径
            disable_update = True   # 禁用每次都检查模型更新
        )
    return _asr_model



def transcribe_audio(file_path:str):
    model = get_asr_model()
    start = time.time()
    result = model.generate(input = file_path)
    text = result[0]["text"]
    elapsed = time.time() - start
    return text, elapsed

