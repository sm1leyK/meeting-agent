# Meeting Agent

一个从零实现的 Python 会议智能助手，用于学习和实践 LLM Application、长文本处理、结构化输出、会话持久化与 Retrieval-Augmented Generation（RAG）。

当前项目已经支持两条主要能力：

1. **Meeting Summarization**
   对完整会议记录进行长文本解析、分块、Map-Reduce 总结，并生成结构化会议纪要。

2. **Meeting RAG Chat**
   将会议文本构建为本地知识库，通过 Embedding、Cosine Similarity 与 Top-K Retrieval 实现基于会议内容的问答，同时支持普通聊天与 RAG 的自动路由。

本项目主要用于学习，因此现阶段尽量避免直接使用 LangChain、LangGraph 等高级框架，而是使用原生 Python、NumPy、SQLAlchemy 等工具手动实现核心流程，以理解 LLM Application / Agent 背后的基本机制。

---

## Current Version

当前开发阶段：

```text
v0.4 — Retrieval-Augmented Generation
```

已经完成：

```text
v0.1  Basic Meeting Summarization
v0.2  Long Meeting Processing
v0.3  Structured Output + Persistent Chat
v0.4  Retrieval-Augmented Generation
```

下一阶段：

```text
v0.5  Agent Workflow
```

---

# Features

## Meeting Summarization

目前支持：

* 读取会议 Transcript
* 自定义 User Instruction
* System Prompt / User Prompt 分离
* Transcript Parsing
* Speaker-aware Chunking
* Token-aware Chunking
* Context Budget Control
* Map-Reduce Summarization
* Recursive Reduce
* Structured JSON Output
* Pydantic Schema Validation
* Structured Output Retry
* 最终结构化会议纪要生成

最终会议摘要使用 `MeetingSummary` Schema，包括：

```text
meeting_topic
main_discussions
key_facts
opinions_and_questions
decisions
action_items
```

---

## Persistent Chat

项目已经实现基本聊天 Session 与 SQLite 持久化。

支持：

* 创建聊天 Session
* 保存 User / Assistant Message
* 加载聊天历史
* 限制传入 LLM 的历史轮数
* Session 列表
* Session 删除
* SQLite 持久化
* SQLAlchemy ORM
* User Message 在 LLM 调用失败时仍然保留

聊天历史不会因为程序退出而丢失。

---

## Retrieval-Augmented Generation

v0.4 已经实现一个不依赖向量数据库框架的最小 RAG Pipeline。

支持：

* 文档句子级 Chunking
* Token-aware Chunking
* Chunk Overlap
* 超长句 Token 级兜底切分
* Multilingual Embedding
* NumPy Vector Store
* Cosine Similarity
* Top-K Retrieval
* Context Construction
* RAG Question Answering
* RAG / Normal Chat 自动路由
* RAG 与 Chat Session 集成

当前 Embedding Model：

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Embedding Dimension：

```text
384
```

---

# Architecture

当前项目主要分为四层：

```text
Meeting Agent
│
├── Meeting Processing
│   ├── Transcript Parsing
│   ├── Token-aware Chunking
│   ├── Map Summarization
│   ├── Recursive Reduce
│   └── Structured Output
│
├── RAG
│   ├── Document Chunking
│   ├── Embedding
│   ├── Vector Store
│   ├── Similarity Search
│   └── Context Construction
│
├── Chat
│   ├── Session
│   ├── History
│   ├── SQLite Persistence
│   └── RAG Routing
│
└── Core
    ├── LLM Interface
    ├── Tokenizer
    ├── Structured LLM Utilities
    └── Schemas
```

---

# Project Structure

```text
meeting-agent/
│
├── app.py
│
├── prompts/
│   ├── system_prompt.txt
│   ├── chunk_prompt.txt
│   ├── merge_prompt.txt
│   └── user_instruction.txt
│
├── data/
│   ├── meeting.txt
│   └── meeting_agent.db
│
├── outputs/
│
├── tokenizers/
│   ├── tokenizer.json
│   └── tokenizer_config.json
│
├── src/
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── io_utils.py
│   │
│   ├── core/
│   │   ├── llm.py
│   │   ├── llm_utils.py
│   │   ├── schemas.py
│   │   └── token_utils.py
│   │
│   ├── meeting/
│   │   ├── meeting.py
│   │   ├── text_splitter.py
│   │   └── transcript_parser.py
│   │
│   ├── chat/
│   │   ├── chat.py
│   │   ├── models.py
│   │   └── storage.py
│   │
│   └── rag/
│       ├── __init__.py
│       ├── chunking.py
│       ├── embedding.py
│       ├── vector_store.py
│       ├── context.py
│       └── rag.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Meeting Summarization Pipeline

完整会议总结流程：

```text
Raw Meeting Transcript
        ↓
load_txt()
        ↓
parse_transcript()
        ↓
Structured Messages
        ↓
prepare_context_budget()
        ↓
Token-aware Chunking
        ↓
Chunks
        ↓
Map
        ↓
Partial Structured Summaries
        ↓
Recursive Reduce
        ↓
Final Structured Summary
        ↓
MeetingSummary
```

---

## Transcript Parsing

当前主要支持：

```text
Speaker(00:00:00): Content
```

例如：

```text
Mason(00:03:01): Yeah, the grant.
```

转换为：

```python
{
    "speaker": "Mason",
    "timestamp": "00:03:01",
    "content": "Yeah, the grant."
}
```

最终会议记录表示为：

```python
list[dict]
```

---

# Token-aware Chunking

会议总结与 RAG 使用不同的 Chunking 逻辑。

## Meeting Chunking

会议 Transcript 已经具有：

```text
speaker
timestamp
content
```

因此会议 Chunker 会尽量保证：

* 不拆断单条 Speaker Message
* 保留 Speaker
* 保留 Timestamp
* 保持发言顺序
* 根据 Token Budget 控制 Chunk 大小

---

## RAG Chunking

RAG 面向普通文本，因此采用：

```text
Document
↓
Sentence Split
↓
Token Count
↓
Chunk Accumulation
↓
Overlap
```

如果单个句子本身超过 `max_tokens`：

```text
Long Sentence
↓
Tokenizer Encode
↓
Token-level Split
↓
Tokenizer Decode
```

Token-level split 只作为最后的 fallback，以尽量避免破坏自然语言边界。

---

# Token Counting

项目使用本地 DeepSeek Tokenizer 计算 Token 数。

```text
Text
↓
DeepSeek Tokenizer
↓
Token IDs
↓
count_tokens()
↓
Token Count
```

Token 计数用于：

* Meeting Chunk Size
* Prompt Size
* Context Budget
* Long Text Processing
* RAG Chunking

---

# Context Budget

会议长文本处理并不是简单限制 Chunk 大小。

完整预算：

```text
input_tokens
+
reserved_output_tokens
+
safety_margin
<
context_limit
```

首先计算：

```text
fixed_prompt_tokens
=
system_prompt_tokens
+
chunk_prompt_tokens
```

然后：

```text
available_chunk_tokens
=
context_limit
- fixed_prompt_tokens
- reserved_output_tokens
- safety_margin
```

最终：

```text
effective_chunk_limit
=
min(
    available_chunk_tokens,
    preferred_chunk_limit
)
```

再将 `effective_chunk_limit` 传给会议 Chunker。

---

# Map-Reduce Summarization

## Map

每个会议 Chunk 独立生成结构化局部摘要：

```text
Chunk 1 → Summary 1
Chunk 2 → Summary 2
Chunk 3 → Summary 3
...
```

每个 Chunk 都经过：

```text
System Prompt
+
Chunk Prompt
+
Chunk Text
↓
LLM
↓
Structured Summary
```

---

## Reduce

多个局部摘要进一步合并：

```text
Partial Summaries
↓
merge_summaries()
↓
Merged Summary
```

如果合并后的文本仍然过长，则继续递归 Reduce：

```text
Summaries
↓
Group
↓
Merge
↓
Still too large?
├── Yes → Reduce again
└── No  → Final Summary
```

最终生成完整会议纪要。

---

# Structured Output

v0.3 将自由文本输出升级为了结构化输出。

当前使用：

```text
LLM
↓
JSON String
↓
json.loads()
↓
dict
↓
Pydantic Validation
↓
MeetingSummary
```

如果出现：

```text
JSONDecodeError
```

或：

```text
ValidationError
```

系统可以重新请求模型生成符合 Schema 的输出。

当前 Schema：

```python
MeetingSummary

meeting_topic: str
main_discussions: list[str]
key_facts: list[str]
opinions_and_questions: list[str]
decisions: list[str]
action_items: list[str]
```

---

# Chat and Persistence

Chat 使用 Session 组织多轮对话。

流程：

```text
session_id
↓
load_history()
↓
build_chat_messages()
↓
save user message
↓
call_llm()
↓
save assistant message
```

User Message 会在 LLM 调用前保存。

因此如果模型调用失败：

```text
User Message
✅ retained

Assistant Message
❌ not created
```

当前持久化使用：

```text
SQLite
+
SQLAlchemy ORM
```

主要数据结构：

```text
ConversationSession
    ↓
ChatMessage
```

Session 删除时，其所属 ChatMessage 会通过 ORM Cascade 一并删除。

---

# RAG Pipeline

v0.4 的核心流程：

```text
Document
↓
Chunking
↓
Embedding
↓
Vector Store
```

查询时：

```text
User Query
↓
Query Embedding
↓
Cosine Similarity
↓
Top-K Retrieval
↓
Relevant Chunks
↓
Context Construction
↓
LLM
↓
Answer
```

---

# Embedding

文本通过：

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

转换为：

```text
384-dimensional vector
```

例如：

```text
"K负责实现RAG模块"
↓
Embedding Model
↓
[0.12, -0.31, 0.08, ...]
```

多个 Chunk：

```text
n chunks
↓
embed_chunks()
↓
shape = (n, 384)
```

---

# Vector Store

目前为了理解向量检索原理，没有直接使用 FAISS、Chroma 或其他 Vector Database。

项目手动实现了一个最小 `VectorStore`：

```text
chunks
+
embeddings
```

支持：

* 添加 Chunk
* 添加 Embedding
* 数量一致性检查
* NumPy Vector Concatenation
* Cosine Similarity Search
* Top-K Retrieval

以后可以替换为：

* FAISS
* Chroma
* pgvector
* Milvus
* Pinecone
* Weaviate

---

# Cosine Similarity

Query Vector 与所有 Chunk Embedding 计算余弦相似度：

```text
query_vector
      ↓
VectorStore Embeddings
      ↓
Cosine Similarity
      ↓
Similarity Scores
      ↓
argsort()
      ↓
Top-K
```

当前实现使用 NumPy，因此可以一次性计算 Query 与所有 Chunk 的相似度。

---

# RAG / Chat Routing

当前 Chat 会先进行 Retrieval：

```text
User Query
↓
Embedding
↓
Top-1 Similarity
↓
Threshold
```

如果：

```text
score >= threshold
```

则进入：

```text
RAG
```

否则进入：

```text
Normal Chat
```

因此：

```text
Meeting-related Question
→ RAG

General Question
→ Normal Chat
```

---

## Important Limitation

当前路由仍然属于 **experimental heuristic**。

真实会议测试发现：

* 某些与知识库无关的问题仍可能获得较高 Cosine Similarity
* 某些真正相关的问题可能只获得较低 Similarity
* 固定 Threshold 无法稳定区分所有 Query

例如，一个知识库中的：

```text
linear regression
```

可能会导致：

```text
“怎么学习线性代数？”
```

获得较高相似度，尽管知识库实际上不能回答这个问题。

因此：

```text
Cosine Similarity
≠
Knowledge Base Answerability
```

未来将考虑更可靠的 Routing 方法。

---

# Global Questions vs Local Retrieval

当前 RAG 更适合：

```text
“Alex 后续需要做什么？”
“谁介绍了这篇论文？”
“项目里提到了什么模型？”
```

这类局部事实问题。

对于：

```text
“整个会议主要讨论了什么？”
```

这种全文总结问题，Top-K Retrieval 可能只看到整份会议的一小部分。

因此当前项目中：

```text
Global Meeting Summary
→ Meeting Summarization Pipeline

Local Meeting Question
→ RAG
```

这两种能力是互补关系，而不是互相替代。

---

# Application Entry

当前 `app.py` 作为一个轻量 CLI 入口。

运行：

```bash
python app.py
```

可以提供类似：

```text
===== Meeting Agent =====

1. Summarize meeting
2. Chat with meeting
3. Exit
```

其中：

```text
Summarize meeting
→ summarize_long_meeting()

Chat with meeting
→ build RAG store
→ create session
→ send_message()
```

未来学习 FastAPI 后，可以在保持业务逻辑不变的情况下，将入口升级为 Web API，例如：

```text
POST /summarize
POST /chat
```

---

# Environment Setup

## Clone

```bash
git clone https://github.com/sm1leyK/meeting-agent.git
cd meeting-agent
```

---

## Virtual Environment

```bash
python -m venv .venv
```

macOS / Linux：

```bash
source .venv/bin/activate
```

Windows：

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

主要依赖包括：

```text
openai
python-dotenv
tokenizers
transformers
numpy
pydantic
sqlalchemy
sentence-transformers
```

---

## Environment Variables

在项目根目录创建：

```text
.env
```

内容：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

`.env` 不应提交到 GitHub。

---

# Model

当前 LLM：

```text
DeepSeek API
deepseek-v4-flash
```

当前 Embedding Model：

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

---

# Usage

将会议文本放入：

```text
data/meeting.txt
```

运行：

```bash
python app.py
```

可以选择：

```text
1. Summarize meeting
2. Chat with meeting
3. Exit
```

---

# Roadmap

## v0.1 — Basic Meeting Summarization ✅

完成：

* [x] DeepSeek API
* [x] `.env` API Key
* [x] Basic Prompt Construction
* [x] User Instruction
* [x] Meeting Transcript Input
* [x] Result Saving
* [x] CLI Entry

---

## v0.2 — Long Meeting Processing ✅

完成：

* [x] Transcript Parsing
* [x] Speaker-aware Chunking
* [x] Token-aware Chunking
* [x] DeepSeek Tokenizer
* [x] Context Budget Control
* [x] Map Summarization
* [x] Reduce Summarization
* [x] Recursive Reduce
* [x] Long Meeting End-to-End Pipeline

---

## v0.3 — Structured Output & Persistent Chat ✅

完成：

* [x] JSON Structured Output
* [x] Meeting Summary Schema
* [x] Pydantic Validation
* [x] Structured Retry
* [x] `MeetingSummary`
* [x] Message-based LLM Interface
* [x] Chat History
* [x] Conversation Session
* [x] SQLite Persistence
* [x] SQLAlchemy ORM
* [x] Session Management
* [x] Message Persistence

---

## v0.4 — Retrieval-Augmented Generation ✅

### M1 — Document Chunking ✅

* [x] Sentence-aware splitting
* [x] Token limit
* [x] Chunk overlap
* [x] Long sentence fallback

### M2 — Embedding ✅

* [x] Multilingual SentenceTransformer
* [x] Text Embedding
* [x] Batch Chunk Embedding
* [x] 384-dimensional vectors

### M3 — Vector Store ✅

* [x] Minimal NumPy Vector Store
* [x] Chunk / Embedding Mapping
* [x] Incremental Add
* [x] Input Validation

### M4 — Query Embedding ✅

* [x] Query → Vector

### M5 — Similarity Retrieval ✅

* [x] Cosine Similarity
* [x] NumPy Matrix Operations
* [x] Top-K Retrieval
* [x] Similarity Score Return

### M6 — Context Construction ✅

* [x] Retrieved Results → LLM Context

### M7 — RAG Answering ✅

* [x] Query
* [x] Retrieval
* [x] Context
* [x] LLM Answer
* [x] End-to-End RAG

### M8 — Chat Integration ✅

* [x] RAG integrated into Chat
* [x] Session History
* [x] Automatic RAG / Chat Routing
* [x] Similarity Threshold
* [x] Original User Message Persistence

### M9 — Testing & Cleanup ✅

Tested:

* [x] Empty Vector Store
* [x] `top_k > number of chunks`
* [x] Chunk / Embedding Mismatch
* [x] RAG Branch
* [x] Normal Chat Branch
* [x] Session History
* [x] Real Meeting Transcript
* [x] Retrieval Quality
* [x] Routing Limitations

---

# Future Work

## Multi-turn RAG Query Rewriting

当前 Retrieval 主要使用当前用户输入。

例如：

```text
Previous:
“K负责RAG模块。”

Current:
“那他什么时候完成？”
```

当前 Query：

```text
“那他什么时候完成？”
```

缺少上下文。

未来可以结合 Chat History 改写为：

```text
“K负责的RAG模块什么时候完成？”
```

再进行 Retrieval。

---

## Contextual Retrieval

未来可以让 Retrieval Query 同时考虑：

```text
Recent History
+
Current User Query
```

提高多轮对话中的检索准确度。

---

## Better RAG Routing

当前使用：

```text
Top-1 Cosine Similarity
+
Fixed Threshold
```

作为路由依据。

未来可以尝试：

* Retrieval Score + LLM Relevance Judge
* Dedicated Router
* Intent Classification
* Answerability Classification
* Confidence Calibration

---

## Better Retrieval

未来可以加入：

* Stronger Embedding Models
* BGE
* E5
* Reranking
* Cross Encoder
* Hybrid Search
* BM25
* Metadata Filtering
* MMR

---

## Persistent Vector Store

目前程序启动时需要重新：

```text
Chunk
→ Embed
→ Build VectorStore
```

未来可以持久化：

* Embeddings
* Chunks
* Metadata
* Vector Index

避免重复计算。

---

## Vector Database

当前使用手写 NumPy Vector Store。

未来可以尝试：

* FAISS
* Chroma
* pgvector
* Milvus

---

## FastAPI

当前 `app.py` 是 CLI。

未来可以提供：

```text
POST /summarize
POST /chat
GET /sessions
DELETE /sessions/{id}
```

让 Meeting Agent 成为可调用的 Web Service。

---

## Agent Workflow

v0.5 将开始探索：

```text
User Request
↓
Router
↓
Choose Capability
├── Meeting Summarization
├── RAG
├── Normal Chat
├── Fact Check
├── Email Generation
└── Tools
↓
Execute
↓
Return Result
```

未来也可以进一步研究：

* Agent Harness
* Tool Selection
* Verifier
* Trajectory
* Self-Evolution
* Agent Evaluation

---

# v0.5 — Agent Workflow

计划：

* [ ] Capability Router
* [ ] Tool Calling
* [ ] Meeting Summarization Tool
* [ ] RAG Tool
* [ ] Fact Checking
* [ ] Email Generation
* [ ] Multi-step Workflow
* [ ] Error Handling
* [ ] Logging
* [ ] Evaluation
* [ ] Agent Harness Exploration

---

# Learning Goals

通过这个项目主要学习：

* Python Project Structure
* Virtual Environment
* Environment Variables
* LLM API
* Prompt Engineering
* Message-based LLM Interface
* Transcript Parsing
* Regular Expressions
* Tokenizer
* Token Counting
* Context Window
* Context Budget
* Long Text Processing
* Speaker-aware Chunking
* Map-Reduce
* Structured Output
* JSON
* Pydantic
* SQLAlchemy
* SQLite
* Conversation Persistence
* Embedding
* Vector Representation
* Cosine Similarity
* Top-K Retrieval
* RAG
* Routing
* Agent Workflow

项目会继续优先理解底层机制，再逐步引入成熟框架。

---

# Known Limitations

当前版本主要是学习型实现，还有以下限制：

* RAG Vector Store 仅存于内存
* Embedding 每次启动需要重新计算
* 固定 Similarity Threshold 路由不稳定
* 当前 Embedding Model 的 Retrieval Quality 有限
* 没有 Reranker
* 没有 Hybrid Retrieval
* 没有 Metadata Filtering
* 多轮 RAG 尚未进行 Query Rewriting
* Global Summary Query 不适合单纯依赖 Top-K RAG
* 暂无 Web API
* 暂无 UI
* 暂无系统化 Evaluation Framework

---

# Why No LangChain?

本项目现阶段刻意不依赖 LangChain / LangGraph 完成核心功能。

原因不是这些框架不好，而是这个项目的主要目标之一是理解：

```text
LLM App / Agent Framework
```

内部到底在做什么。

因此目前手动实现：

```text
Prompt
Messages
Token Budget
Chunking
Map-Reduce
Structured Output
Session
Persistence
Embedding
Vector Store
Similarity Search
RAG
Routing
```

等这些概念真正理解后，再使用更高级框架会更容易判断：

* 框架替我做了什么
* 哪些东西值得用框架
* 哪些东西应该自己控制

---

# License

本项目目前主要用于个人学习、实验与课程实践。
