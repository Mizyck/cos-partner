from fastapi import FastAPI
from routers import chat

app = FastAPI(title = "AI 角色扮演")

app.include_router(chat.router, prefix = "/chat")

@app.get("/")
def read_root():
    return {"msg": "hello fastapi"}

@app.get("/ping")
def ping():
    return {"msg": "pong"}
