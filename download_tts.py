import os
from modelscope import snapshot_download

def main():
    model_dir = os.path.join(os.getcwd(), "models", "tts", "CosyVoice2-0.5B")
    os.makedirs(model_dir, exist_ok=True)
    os.environ["MODELSCOPE_CACHE"] = model_dir
    snapshot_download('iic/CosyVoice2-0.5B', local_dir=model_dir)
    print("CosyVoice2-0.5B 下载完成")

if __name__ == "__main__":
    main()
