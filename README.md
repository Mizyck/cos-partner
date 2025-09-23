# cos-LLM

AI 角色扮演

## 启动方式
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
接口说明
GET / → 返回 {"msg": "hello fastapi"}

GET /ping → 健康检查

POST /chat/
