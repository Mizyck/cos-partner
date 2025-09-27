import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

class Settings:
    QINIU_API_KEY: str = os.getenv("QINIU_API_KEY")
    QINIU_BASE_URL: str = "https://openai.qiniu.com/v1"

settings = Settings()
