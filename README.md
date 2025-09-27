# cos-LLM / cos-partner

AI 角色扮演项目 —— 基于 FastAPI 的后端服务。  
目标：提供角色扮演对话接口，支持前端调用，后续可接入大语言模型与语音合成。

---

## 快速开始

### 1. 克隆项目
```bash
git clone git@github.com:Mizyck/cos-partner.git
cd cos-partner
```

### 2. 安装依赖

建议使用conda创建虚拟环境：
```bash
conda create -n cos-llm python=3.10 -y
conda activate cos-llm

# 安装基础依赖
pip install -r requirements.txt
```
根据你的环境选择适合的torch版本：

CPU：
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```
GPU：
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```
下载tts

### 3. 启动服务
```bash
uvicorn main:app --reload --port 8000
```

启动后访问：

Swagger 文档: http://127.0.0.1:8000/docs

健康检查: http://127.0.0.1:8000/ping

## 接口说明

### 返回服务状态：
```bash
{ "msg": "hello fastapi" }
```

### GET /ping
健康检查：
```bash
{ "status": "ok" }
```

### POST /chat/
角色对话接口（目前仍为mock返回，后续接入模型）
请求示例：
```bash
{
  "user_input": "你好",
  "role": "界徐盛"
}
```
响应示例：
```bash
{
  "role": "界徐盛",
  "reply": "界徐盛 回答：你好的回答",
}
```
### POST /asr/
语音识别接口，采用FunASR
请求方式： 
```bash
POST /asr/
```
请求参数：音频文件（form-data）

响应示例：
```bash
{
  "text": "...",
  "status": "success"
}
```


## 项目结构
```bash
cos-partner/
├── main.py              # 入口文件
├── routers/             # 路由模块
│   ├── chat.py
│   └── asr.py
├── services/            # 服务逻辑
│   ├── llm_service.py   # 模型调用（目前 mock）
│   └── asr_service.py   # asr模型调用
├── requirements.txt     # 依赖
├── README.md            # 项目说明
└── .gitignore
```
