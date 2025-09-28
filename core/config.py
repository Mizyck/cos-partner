import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

class Settings:
    QINIU_API_KEY: str = os.getenv("QINIU_API_KEY")
    QINIU_BASE_URL: str = "https://openai.qiniu.com/v1"     # 默认使用七牛云接口，可自行修改

settings = Settings()
