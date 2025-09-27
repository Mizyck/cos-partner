from openai import OpenAI
from core.config import settings

client = OpenAI(
    api_key=settings.QINIU_API_KEY,
    base_url=settings.QINIU_BASE_URL
)


def call_llm(user_input: str, role:str = "default") -> str:
    # 接入模型
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content