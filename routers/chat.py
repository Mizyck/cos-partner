from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import call_llm

router = APIRouter()

# 定义请求体模型
class ChatRequest(BaseModel):
    user_input: str
    role: str = "界徐盛"

@router.post("/")
def chat(req: ChatRequest):
    reply = call_llm(req.user_input, req.role)
    return {"role": req.role, "reply":reply}

