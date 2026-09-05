# Meeting Agent

一个轻量级的 Python 会议助手，使用大语言模型根据会议记录生成结构化会议纪要。

本项目目前主要作为一个 LLM 应用开发学习项目，用于从底层理解 Prompt 设计、API 调用、会议文本解析、长文本切分、Token 预算控制、Map-Reduce 总结，以及后续的结构化输出、RAG 检索问答与 Agent Workflow。

Meeting Agent 基于 Python 与 DeepSeek API 从零实现，现阶段尽量避免直接依赖 LangChain 等高级框架，而是优先手动实现核心模块，以理解 LLM Application / Agent 背后的基础工作原理。

## 功能

目前已完成：

* 从文本文件读取会议记录
* 调用 DeepSeek API 处理会议内容
* 生成结构化会议纪要
* 支持自定义用户指令
* 分离 System Prompt、User Instruction 与 Meeting Transcript
* 使用 `.env` 管理 API Key
* 基础模块化项目结构
* 会议转录文本解析
* Speaker-aware Chunking
* 基于 DeepSeek V4 Tokenizer 的 Token 计数
* Token-aware Chunking
* Context Budget Control
* 基于 Chunk 的局部会议总结
* Map 阶段长会议摘要处理

计划实现：

* Map-Reduce 中的 Reduce 阶段
* 结构化 JSON 输出
* 基于 Embedding 的语义检索
* 基于 RAG 的会议内容问答
* 向量检索
* 科研邮件生成
* 会议纪要事实核查
* 简单用户界面
* 更通用的会议转录格式识别

## 项目结构

```text
meeting-agent/

├── data/
│   ├── meeting.txt
│   ├── example_meeting.txt
│   └── user_instruction.txt
│
├── outputs/
│
├── prompts/
│   ├── system_prompt.txt
│   └── chunk_prompt.txt
│
├── tokenizers/
│   ├── tokenizer.json
│   └── tokenizer_config.json
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── io_utils.py
│   ├── llm.py
│   ├── meeting.py
│   ├── text_splitter.py
│   ├── token_utils.py
│   └── transcript_parser.py
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 工作流程

当前项目已经同时支持基础短会议流程与长会议处理流程。

### 基础会议总结流程

```text
Meeting Transcript
        ↓
load_txt()
        ↓
build_user_prompt()
        ↓
System Prompt + User Prompt
        ↓
call_llm()
        ↓
Meeting Summary
        ↓
save_result()
```

其中：

```text
System Prompt
    ↓
定义助手长期保持的角色、事实约束与行为规则

User Instruction
    ↓
定义用户本次具体希望完成的任务

Meeting Transcript
    ↓
提供需要处理的会议原始数据
```

同一份会议记录可以通过不同 User Instruction 完成不同任务，例如：

* 生成完整会议纪要
* 提取行动项
* 提取导师意见
* 查找尚未解决的问题
* 分析会议中的不同观点
* 生成其他结构化内容

项目中的一个核心设计思路是：

> 会议记录是数据，Prompt 决定如何处理这些数据。

### 长会议处理流程

```text
Raw Meeting Transcript
        ↓
load_txt()
        ↓
parse_transcript()
        ↓
Structured Messages
        ↓
prepare_chunk_budget()
        ↓
effective_chunk_limit
        ↓
chunk_messages()
        ↓
Chunks
        ↓
format_chunk()
        ↓
summarize_chunks()
        ↓
Partial Summaries
```

当前已完成 Map 阶段，后续将在 Reduce 阶段将多个局部摘要合并为最终会议纪要。

## Prompt 设计

当前项目将 Prompt 分为不同职责层级。

### System Prompt

用于定义模型长期保持的角色与约束，例如：

* 作为严谨的会议内容处理助手
* 不得编造会议中不存在的信息
* 区分事实、个人建议、讨论方向、明确决定与后续行动
* 不得自行补充负责人、截止时间或结论
* 对疑似 ASR 转写错误保持谨慎
* 当前会议片段不足以支持结论时，应明确标记不确定性

### User Instruction

用于表达用户本次具体想完成的任务，例如：

```text
请生成结构化会议纪要，重点包括：

1. 当前研究进展
2. 当前问题
3. 导师意见
4. 已明确决定的事项
5. 后续行动项
```

会议原文会作为数据与 User Instruction 一起加入 User Prompt。

### Chunk Prompt

长会议被切分后，Chunk Prompt 用于指导模型处理单个会议片段。

其主要职责包括：

* 提取当前片段的主要讨论内容
* 保留关键事实与研究进展
* 区分观点、建议、决定与行动项
* 避免把当前状态误写成后续行动
* 对 ASR 转写错误与实体名称保持谨慎
* 为后续 Reduce 阶段保留足够信息

当前 Map 阶段的实际 Prompt 结构：

```text
System Role:
system_prompt.txt

User Role:
chunk_prompt.txt
+
当前会议片段
```

## Transcript Parsing

会议转录文本首先经过解析器转换为统一的数据结构。

当前支持格式：

```text
Speaker(00:00:00): Content
```

例如：

```text
陈杰(00:03:01): Yeah, the grant.
```

解析后：

```python
{
    "speaker": "陈杰",
    "timestamp": "00:03:01",
    "content": "Yeah, the grant."
}
```

多个发言最终表示为：

```python
list[dict]
```

示意：

```python
[
    {
        "speaker": "...",
        "timestamp": "...",
        "content": "..."
    },
    ...
]
```

后续计划扩展对不同会议平台、ASR 工具和 Transcript 格式的识别。

## Chunking

为了处理较长会议文本，项目实现了 Speaker-aware Chunking。

核心原则：

* 尽量保持单条发言完整
* 不直接按固定字符位置切断发言
* 按会议发言顺序进行累积
* 超过当前 Chunk 上限时创建新的 Chunk

结构：

```text
Structured Messages
        ↓
chunk_messages()
        ↓
List[List[Message]]
```

之后通过：

```text
format_chunk()
```

将结构化数据重新转换为：

```text
Speaker(timestamp): content
```

形式的文本，供 LLM 使用。

## Token Counting

早期版本使用字符数控制 Chunk 大小：

```text
len(text)
```

当前已升级为基于 DeepSeek V4 Tokenizer 的真实 Token 计数：

```text
text
    ↓
DeepSeek V4 Tokenizer
    ↓
Token IDs
    ↓
count_tokens()
    ↓
Token Count
```

项目使用 DeepSeek 官方提供的 `tokenizer.json` 进行本地 Token 计算。

Token 计数主要用于：

* Chunk 大小控制
* Prompt Token 计算
* Context Budget 估算
* 后续 API 成本统计与上下文管理

## Context Budget Control

仅限制 Chunk 本身的 Token 数仍不足以保证完整请求不会超过模型上下文长度。

因此项目进一步加入 Context Budget Control。

当前使用的基本约束：

```text
input_tokens
+
reserved_output_tokens
+
safety_margin
<
context_limit
```

其中：

```text
fixed_prompt_tokens
=
system_prompt_tokens
+
chunk_prompt_tokens
```

理论上可用于会议 Chunk 的空间：

```text
available_chunk_tokens
=
context_limit
- fixed_prompt_tokens
- reserved_output_tokens
- safety_margin
```

同时，为避免单个 Chunk 过大，项目额外设置：

```text
preferred_chunk_limit
```

最终实际使用：

```text
effective_chunk_limit
=
min(
    available_chunk_tokens,
    preferred_chunk_limit
)
```

当前默认配置：

```text
context_limit = 1,000,000
reserved_output_tokens = 4,000
safety_margin = 1,000
preferred_chunk_limit = 8,000
```

`effective_chunk_limit` 最终传入 `chunk_messages()` 作为实际 Chunk Token 上限。

## Map Summarization

当前已经完成 Map 阶段。

对于多个 Chunk：

```text
chunk 1 → summary 1
chunk 2 → summary 2
chunk 3 → summary 3
...
```

核心流程：

```text
Chunk
↓
format_chunk()
↓
System Prompt
+
Chunk Prompt
+
Chunk Text
↓
call_llm()
↓
Partial Summary
```

多个 Partial Summary 将在后续 Reduce 阶段进一步合并。

## 环境配置

### 1. 克隆仓库

```bash
git clone <你的仓库地址>

cd meeting-agent
```

### 2. 创建虚拟环境

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

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

目前主要依赖：

```text
openai
python-dotenv
transformers
tokenizers
```

### 4. 配置环境变量

在项目根目录创建 `.env`：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

`.env` 中包含 API Key，不应上传到 GitHub。

### 5. 配置 DeepSeek Tokenizer

从 DeepSeek 官方 API 文档下载 DeepSeek V4 Tokenizer，并将相关文件放入：

```text
tokenizers/
```

例如：

```text
tokenizers/
├── tokenizer.json
└── tokenizer_config.json
```

当前项目实际通过 `tokenizer.json` 加载本地 Tokenizer。

## 使用方法

将会议记录放入：

```text
data/meeting.txt
```

然后运行：

```bash
python app.py
```

程序会根据当前流程：

```text
读取会议记录
↓
解析 Transcript
↓
计算 Token Budget
↓
进行 Chunking
↓
逐 Chunk 调用 LLM
↓
返回局部结构化摘要
```

短会议仍可直接使用基础总结流程。

## 当前开发阶段

项目已经从最基础的：

```text
Input
→ Prompt
→ LLM API
→ Response
```

逐步扩展为：

```text
Transcript
→ Parse
→ Tokenize
→ Budget
→ Chunk
→ Map Summarization
```

当前阶段暂时不使用 LangChain 等高级框架，而是优先自行实现底层流程。

后续将在此基础上继续实现：

```text
Reduce
→ Structured Output
→ RAG
→ Fact Check
→ Agent Workflow
```

# Roadmap

## v0.1 — Basic Meeting Summarization ✅

完成基础会议总结流程：

* [x] 使用 DeepSeek API 调用大语言模型
* [x] 使用 `.env` 管理 API Key
* [x] 将模型调用封装至 `llm.py`
* [x] 分离 System Prompt、User Instruction 与 Meeting Transcript
* [x] 支持自定义 `user_instruction`
* [x] 将会议总结结果保存为 Markdown 文件
* [x] 使用 `app.py` 作为程序入口

基础流程：

```text
meeting.txt
    ↓
build_user_prompt()
    ↓
call_llm()
    ↓
meeting summary
    ↓
save_result()
```

---

## v0.2 — Long Meeting Processing 🚧

目标：支持较长的会议转录文本，并逐步解决上下文长度限制、会议语义连续性与多阶段总结问题。

### v0.2.1 — Transcript Parsing ✅

将原始会议转录文本解析为统一结构。

当前支持：

```text
Speaker(00:00:00): Content
```

解析后：

```python
{
    "speaker": "...",
    "timestamp": "...",
    "content": "..."
}
```

已完成：

* [x] 使用正则表达式识别会议发言
* [x] 提取 speaker
* [x] 提取 timestamp
* [x] 提取 content
* [x] 将 transcript 转换为 `list[dict]`

流程：

```text
Raw Transcript
      ↓
parse_transcript()
      ↓
Structured Messages
```

未来将扩展对不同 Transcript 格式的识别。

---

### v0.2.2 — Speaker-aware Chunking ✅

在不拆断单条发言的前提下，将结构化会议记录划分为多个 Chunk。

已完成：

* [x] 实现 `chunk_messages()`
* [x] 保证单条 Speaker Message 尽量保持完整
* [x] 避免 Message 在 Chunk 切换时丢失
* [x] 处理最后一个未满 Chunk
* [x] 实现 `format_chunk()`
* [x] 将结构化 Message 恢复为会议文本

流程：

```text
Structured Messages
        ↓
chunk_messages()
        ↓
List[List[Message]]
        ↓
format_chunk()
        ↓
Formatted Chunk Text
```

早期版本使用字符数作为 Chunk 大小依据。

当前已在 v0.2.3 中升级为 Token-aware Chunking。

---

### v0.2.3 — Token-aware Chunking ✅

将字符长度控制升级为基于 DeepSeek Tokenizer 的 Token 长度控制，并加入完整 Context Budget 管理。

#### v0.2.3.1 — Token Counting ✅

已完成：

* [x] 接入 DeepSeek V4 Tokenizer
* [x] 使用官方 `tokenizer.json`
* [x] 实现 `count_tokens()`
* [x] 将 `max_char` 替换为 `max_tokens`
* [x] 根据实际格式化后的 Message 计算 Token 数
* [x] 保持原有 Speaker-aware Chunking 逻辑

升级过程：

```text
len(text)
    ↓
count_tokens(text)
```

使 Chunk 大小与实际 LLM 上下文消耗更加一致。

---

#### v0.2.3.2 — Context Budget Control ✅

在 Chunk 大小之外，进一步考虑完整请求的上下文预算。

目标约束：

```text
input_tokens
+
reserved_output_tokens
+
safety_margin
<
context_limit
```

已完成：

* [x] 为模型输出预留 Token
* [x] 计算 System Prompt Token 占用
* [x] 计算 Chunk Prompt Token 占用
* [x] 计算 Fixed Prompt Token 占用
* [x] 计算可用于 Meeting Chunk 的 Token Budget
* [x] 加入 Safety Margin
* [x] 设置 Preferred Chunk Limit
* [x] 计算 Effective Chunk Limit
* [x] 将最终 Token Limit 接入 `chunk_messages()`

当前流程：

```text
system_prompt_tokens
+
chunk_prompt_tokens
        ↓
fixed_prompt_tokens
        ↓
context_limit
- fixed_prompt_tokens
- reserved_output_tokens
- safety_margin
        ↓
available_chunk_tokens
        ↓
min(
    available_chunk_tokens,
    preferred_chunk_limit
)
        ↓
effective_chunk_limit
        ↓
chunk_messages()
```

---

### v0.2.4 — Map-Reduce Meeting Summarization 🚧

针对多个会议 Chunk 分阶段完成会议总结。

#### Map ✅

当前已完成基础版本：

* [x] 实现 `summarize_chunk()`
* [x] 实现 `summarize_chunks()`
* [x] 为每个 Chunk 独立调用 LLM
* [x] 使用独立 `system_prompt`
* [x] 使用专用 `chunk_prompt`
* [x] 将 Chunk Prompt 与当前会议片段组合为 User Prompt
* [x] 保留关键事实、建议、决定和行动项
* [x] 对 ASR 转写不确定信息增加约束
* [x] 区分当前状态与真正的后续行动

流程：

```text
chunk 1
↓
summary 1

chunk 2
↓
summary 2

chunk 3
↓
summary 3
```

单个 Chunk 的 Prompt 结构：

```text
System:
system_prompt

User:
chunk_prompt
+
chunk_text
```

#### Reduce 🚧

计划：

* [ ] 实现 `merge_summaries()`
* [ ] 设计独立 `merge_prompt`
* [ ] 合并多个局部摘要
* [ ] 去除重复信息
* [ ] 保留跨 Chunk 的讨论关系
* [ ] 避免局部信息在合并过程中失真
* [ ] 重新应用用户最终 `user_instruction`
* [ ] 生成最终会议纪要

完整目标流程：

```text
meeting.txt
    ↓
parse_transcript()
    ↓
messages
    ↓
prepare_chunk_budget()
    ↓
effective_chunk_limit
    ↓
chunk_messages()
    ↓
chunks
    ↓
summarize_chunks()
    ↓
partial summaries
    ↓
merge_summaries()
    ↓
final meeting summary
```

---

## v0.3 — Structured Output

目标：让模型输出从自由文本升级为稳定的数据结构。

计划：

* [ ] JSON Structured Output
* [ ] 定义 Meeting Summary Schema
* [ ] 使用 Pydantic 进行数据验证
* [ ] 结构化表示：

  * Topics
  * Decisions
  * Action Items
  * Participants
  * Open Questions
* [ ] 处理格式错误与模型输出异常
* [ ] 为后续 RAG、Fact Check 和 Agent Workflow 提供稳定数据结构

示例：

```json
{
  "topics": [],
  "decisions": [],
  "action_items": [],
  "open_questions": []
}
```

---

## v0.4 — Retrieval-Augmented Generation (RAG)

目标：让会议助手能够利用外部知识库与历史会议辅助理解当前会议内容。

计划：

* [ ] 学习 Embedding
* [ ] 使用 NumPy 实现 Cosine Similarity
* [ ] 实现 Top-K Retrieval
* [ ] 构建最小可用 RAG Pipeline
* [ ] 使用 FAISS 管理向量索引
* [ ] 支持会议相关术语检索
* [ ] 支持项目背景检索
* [ ] 支持历史会议检索
* [ ] 支持基于会议内容的问答

流程：

```text
User Query / Meeting
        ↓
Embedding
        ↓
Vector Retrieval
        ↓
Relevant Context
        ↓
LLM
```

---

## v0.5 — Meeting Agent Workflow

目标：从“会议总结工具”进一步发展为完整 Meeting Agent。

计划加入：

* [ ] Meeting Summary
* [ ] Research Progress Extraction
* [ ] Action Item Extraction
* [ ] Meeting Email Generation
* [ ] Fact Checking
* [ ] Historical Meeting Retrieval
* [ ] Multi-step Workflow
* [ ] Error Handling
* [ ] Logging
* [ ] API Usage Statistics
* [ ] Token Usage Statistics

可能的完整流程：

```text
Transcript
    ↓
Parse
    ↓
Token Budget
    ↓
Chunk
    ↓
Summarize
    ↓
Merge
    ↓
Structured Output
    ↓
Fact Check
    ↓
Meeting Knowledge
    ↓
Email / Report / Query
```

---

## Future

在完成底层实现并理解各模块原理之后，再考虑使用更高级的 LLM 应用框架：

* LangChain
* LangGraph
* Agent Frameworks

本项目现阶段优先通过原生 Python 实现核心功能，以理解 LLM Application / Agent 各模块背后的工作原理，而不是直接依赖框架封装。

## 学习目标

通过这个项目，希望逐步掌握：

* Python 项目结构
* 虚拟环境与依赖管理
* `.env` 与环境变量
* LLM API 调用
* Prompt Engineering
* System Prompt 与 User Prompt
* 模块化程序设计
* 正则表达式基础
* Transcript Parsing
* 长文本处理
* Tokenizer
* Token Counting
* Context Window
* Context Budget
* Speaker-aware Chunking
* Map-Reduce Summarization
* Structured Output
* Pydantic
* Embedding
* 向量检索
* Retrieval-Augmented Generation（RAG）
* Fact Checking
* LLM Agent
* Agent Workflow

项目早期会尽量避免直接使用高级框架封装核心流程，希望先理解这些技术底层到底是如何工作的。

## License

本项目目前主要用于个人学习与实验。
