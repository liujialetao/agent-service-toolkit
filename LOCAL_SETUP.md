# 本地运行说明

> 本文件记录本机上的安装与配置状态，便于在新对话中快速恢复上下文。  
> **不含 API Key**；密钥仅保存在 `.env`（已在 `.gitignore` 中）。

## 项目信息

| 项 | 值 |
|---|---|
| 仓库 | [JoshuaC215/agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) |
| 本地路径 | `/Users/liujia/code/learn/rag/githubDemos/agent-service-toolkit` |
| 定位 | LangGraph + FastAPI + Streamlit 学习用 Agent 项目 |
| Python | 3.12（由 `uv` 管理，虚拟环境在 `.venv`） |

## 已完成的步骤

- [x] `git clone` 到上述路径
- [x] `uv sync --frozen --python 3.12`（依赖已安装）
- [x] 创建 `.env`（见下方配置摘要）
- [x] 曾用 `USE_FAKE_MODEL=true` 验证服务可启动
- [x] 已切换为阿里云百炼 OpenAI 兼容模式

## `.env` 配置摘要

配置文件路径：**项目根目录 `.env`**

```env
USE_FAKE_MODEL=false

# 阿里云百炼 OpenAI 兼容接口
COMPATIBLE_MODEL=qwen-max
COMPATIBLE_API_KEY=<在百炼控制台申请，勿提交到 Git>
COMPATIBLE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DEFAULT_MODEL=openai-compatible

DATABASE_TYPE=sqlite
SQLITE_DB_PATH=checkpoints.db
MODE=dev
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8080
```

### 变量说明

| 变量 | 作用 |
|------|------|
| `COMPATIBLE_MODEL` | 百炼实际模型名（如 `qwen-max`） |
| `COMPATIBLE_API_KEY` | 百炼 API Key |
| `COMPATIBLE_BASE_URL` | 兼容接口地址 |
| `DEFAULT_MODEL` | 固定为 `openai-compatible`（项目内部模型类型，不是百炼模型名） |

Key 申请：https://dashscope.console.aliyun.com/

## 启动与停止

### 启动（两个终端）

```bash
cd /Users/liujia/code/learn/rag/githubDemos/agent-service-toolkit/src

# 终端 1：FastAPI 后端
../.venv/bin/python run_service.py

# 终端 2：Streamlit 前端
../.venv/bin/streamlit run streamlit_app.py
```

### 停止

```bash
pkill -f "run_service.py" 2>/dev/null
pkill -f "streamlit_app.py" 2>/dev/null
```

修改 `.env` 后必须重启上述两个进程。

### Docker 方式（可选）

```bash
cd /Users/liujia/code/learn/rag/githubDemos/agent-service-toolkit
docker compose watch
```

## 访问地址

| 服务 | URL |
|------|-----|
| Streamlit 聊天 UI | http://localhost:8501 |
| FastAPI Swagger | http://localhost:8080/docs |
| Agent 列表与模型 | http://localhost:8080/info |
| 健康检查 | http://localhost:8080/health |

## 验证命令

进程是否在跑、端口是否监听、一键检查等，见 **[learn/01-启动与运行.md § 验证服务是否正常](./learn/01-启动与运行.md#验证服务是否正常)**。

```bash
# 查看可用 Agent 和模型（models 中应有 openai-compatible）
curl -s http://127.0.0.1:8080/info | python3 -m json.tool

# 简单对话测试
curl -s -X POST http://127.0.0.1:8080/chatbot/invoke \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","model":"openai-compatible","thread_id":"test-1"}'
```

## 内置 Agent（学习顺序建议）

| Agent key | 说明 | 建议阅读文件 |
|-----------|------|-------------|
| `chatbot` | 最简单聊天 | `src/agents/chatbot.py` |
| `research-assistant` | 带搜索、计算器等 Tool | `src/agents/research_assistant.py` |
| `rag-assistant` | RAG 问答 | `src/agents/rag_assistant.py`、`docs/RAG_Assistant.md` |
| `langgraph-supervisor-agent` | Supervisor 多 Agent | `src/agents/langgraph_supervisor_agent.py` |

完整列表：`curl http://127.0.0.1:8080/info`

## 关键目录

```
agent-service-toolkit/
├── .env                 # 本地密钥与配置（勿提交）
├── .venv/               # uv 虚拟环境
├── src/
│   ├── agents/          # LangGraph Agent 定义（学习重点）
│   ├── service/         # FastAPI 路由
│   ├── core/            # settings、llm 工厂
│   └── streamlit_app.py # 前端 UI
└── docs/                # 官方文档（含 RAG、Ollama 等）
```

## 与 LangChain-RAG-FastAPI-Service 的关系

| | 当前项目 (agent-service-toolkit) | 原 RAG 笔记项目 |
|--|----------------------------------|----------------|
| Agent 编排 | **LangGraph**（StateGraph） | LangChain `AgentExecutor` |
| 前端 | Streamlit | React |
| RAG | `rag-assistant` + ChromaDB | 完整知识库 + HyDE + 重排序 |
| LLM | 百炼 openai-compatible | 百炼 / Ollama |

## 待办 / 可选

- [ ] 确认 `.env` 中 `COMPATIBLE_API_KEY` 已替换为真实 Key
- [ ] 按 `docs/RAG_Assistant.md` 配置 RAG Agent 并上传文档
- [ ] （可选）配置 `LANGSMITH_API_KEY` 追踪 Agent 执行
- [ ] （可选）安装 Ollama 作为本地备用模型，见 `docs/Ollama.md`
- [ ] （可选）LangGraph Studio：`langgraph dev`（需配置 `langgraph.json`）

## 新对话开场白（复制即用）

```
请先阅读 @LOCAL_SETUP.md 和 @README.md。
我在本地已配置 agent-service-toolkit（百炼 qwen-max + openai-compatible）。
帮我：<你的具体目标>
```
