from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import chat
from routers import asr as asr_router
from routers import tts as tts_router



# 创建 FastAPI 应用
app = FastAPI(title = "AI 角色扮演")
# 静态文件夹，用于存放角色音频文件
app.mount("/voices", StaticFiles(directory="voices"), name="voices")

# 根路由，包含各个子路由
app.include_router(asr_router.router, prefix = "/asr")
app.include_router(tts_router.router, prefix = "/tts")
app.include_router(chat.router, prefix = "/chat")

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.get("/ping")
def ping():
    return {"status": "success"}