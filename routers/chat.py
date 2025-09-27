from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import call_llm

router = APIRouter()

# 定义请求体模型
class ChatRequest(BaseModel):
    user_id: str = "default_user"
    user_input: str
    role: str = "default"

class ChatResponse(BaseModel):
    reply: str

@router.post("/",  response_model = ChatResponse)
async def chat(req: ChatRequest):
    reply = call_llm(req.user_input, req.role)
    return ChatResponse(reply=reply)

