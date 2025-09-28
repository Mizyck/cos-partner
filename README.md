# cos-LLM / cos-partner

AI 角色扮演项目 —— 基于 FastAPI 的后端服务。 目标：提供角色扮演对话接口，支持前端调用，集成 qwen-turbo、FunASR 与 CoquiXTTS-V2，实现沉浸式角色扮演体验。

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
GPU(CUDA11.8)：
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```
下载XTTS模型
```bash
# Make sure git-lfs is installed (https://git-lfs.com)
git lfs install

git clone git@hf.co:coqui/XTTS-v2
```
请将下载的模型文件放置在项目根目录（main.py同级）下的 models/ 内（没有则新建文件夹）。
### 3. 设置大模型API
在.env中设置自己的LLM的API KEY，默认使用七牛云，若使用其他接口可自行在 core/config.py 修改
### 4. 启动服务
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
{ "status": "success" }
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
  "text": "识别结果",
  "status": "success"
}
```
### POST /tts/
语音合成接口（XTTS-v2）
请求参数：
```bash
{
  "text": "待转换文本",
  "language": "zh",
  "speaker_wav": "可选，参考音频路径"
}

```
响应：生成的wv文件路径（服务端临时文件）


## 项目结构
```bash
cos-partner/
├── main.py              # 入口文件
├── routers/             # 路由模块
│   ├── chat.py          # 对话接口
│   ├── asr.py           # 语音识别接口
│   └── tts.py           # 文本转语音接口
├── services/            # 服务逻辑
│   ├── llm_service.py   # llm模型调用（目前 mock）
│   ├── asr_service.py   # asr模型调用
│   └── tts_service.py   # tts模型调用
├── requirements.txt     # 依赖
├── README.md            # 项目说明
└── .gitignore
```
## TODO
接入真实大语言模型

增加上下文记忆与多角色管理

优化 TTS 推理速度，支持流式输出

前端页面集成（WebSocket 实时对话）