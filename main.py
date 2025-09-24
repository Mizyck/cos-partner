from fastapi import FastAPI
from routers import chat
from routers import asr as asr_router

app = FastAPI(title = "AI 角色扮演")

app.include_router(chat.router, prefix = "/chat")
app.include_router(asr_router.router, prefix = "/asr")

@app.get("/")
def read_root():
    return {"msg": "hello fastapi"}

@app.get("/ping")
def ping():
    return {"status": "success"}