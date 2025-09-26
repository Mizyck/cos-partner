from funasr import AutoModel
import time
import os

model_dir = os.path.join(os.getcwd(), "models", "asr")

# 加载模型
asr_model = AutoModel(model = "paraformer-zh", vad_model = "fsmn-vad", punc_model = "ct-punc", cache_dir = model_dir)

def transcribe_audio(file_path:str):
    model = get_asr_model()
    start = time.time()
    result = model.generate(input = file_path)
    text = result[0]["text"]
    elapsed = time.time() - start
    return text, elapsed

