from funasr import AutoModel
import time

# 加载模型
asr_model = AutoModel(model = "paraformer-zh", vad_model = "fsmn-vad", punc_model = "ct-punc")

def transcribe_audio(file_path:str):
    start = time.time()
    result = asr_model.generate(input = file_path)
    text = result[0]["text"]
    elapsed = time.time() - start
    return text, elapsed

