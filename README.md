# Meeting Agent

一个轻量级的 Python 会议助手，使用大语言模型根据会议记录生成结构化会议纪要。

这个项目目前主要作为一个 LLM 应用开发学习项目，用来从底层理解 Prompt 设计、API 调用、会议文本处理，以及后续的 RAG 检索问答等内容。

Meeting Agent 是一个基于 Python 与 DeepSeek API 从零实现的会议智能助手项目。
项目将逐步实现会议转录解析、长文本切分、Map-Reduce 总结、结构化输出、RAG 与 Agent Workflow，并尽量在不依赖高级 Agent 框架的情况下理解和实现各核心模块。

## 功能

目前已完成：

- 从文本文件读取会议记录
- 调用大语言模型处理会议内容
- 生成结构化会议纪要
- 支持自定义用户指令
- 将 System Prompt 与用户任务分离
- 使用 `.env` 管理 API Key
- 基础模块化项目结构

计划实现：

- 长会议文本切块
- 结构化 JSON 输出
- 基于 Embedding 的语义检索
- 基于 RAG 的会议内容问答
- 向量检索
- 科研邮件生成
- 会议纪要事实核查
- 简单用户界面

## 项目结构

```text
meeting-agent/
├── data/
│   └── example_meeting.txt
│
├── outputs/
│
├── prompts/
│   └── system_prompt.txt
│
├── src/
│   ├── config.py
│   ├── llm.py
│   └── meeting.py
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
````

## 工作流程

当前程序的主要流程：

```text
会议记录
   ↓
读取会议文本
   ↓
读取 System Prompt
   ↓
构造 User Prompt
   ↓
调用 LLM API
   ↓
生成结构化会议纪要
```

其中：

```text
System Prompt
    ↓
定义助手的固定角色和行为规则

User Instruction
    ↓
定义用户这一次具体想完成的任务

Meeting Transcript
    ↓
提供需要处理的会议原始数据
```

同一份会议记录可以通过不同的用户指令完成不同任务，例如：

* 生成完整会议纪要
* 提取行动项
* 提取导师意见
* 查找尚未解决的问题
* 分析会议中的不同观点
* 生成其他结构化内容

项目中的一个核心设计思路是：

> 会议记录是数据，Prompt 决定如何处理这些数据。

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
```

### 4. 配置环境变量

在项目根目录创建 `.env`：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

`.env` 中包含 API Key，不应上传到 GitHub。

## 使用方法

将会议记录放入：

```text
data/example_meeting.txt
```

然后运行：

```bash
python app.py
```

程序会读取会议记录，将用户任务和会议内容发送给大语言模型，并返回结构化会议纪要。

## Prompt 设计

当前项目将 Prompt 分成两个主要部分。

### System Prompt

用于定义模型长期保持的角色和规则，例如：

* 作为严谨的会议内容处理助手
* 不得编造会议中不存在的信息
* 区分事实、个人建议、讨论方向和明确决定
* 不得自行补充负责人或截止时间

### User Prompt

用于表达用户这一次具体想完成的任务，例如：

```text
请生成结构化会议纪要，重点包括：
1. 当前研究进展
2. 当前问题
3. 导师意见
4. 已明确决定的事项
5. 后续行动项
```

会议原文会作为数据一起加入 User Prompt 中。

## 当前开发阶段

目前项目主要关注最基础的 LLM 调用流程：

```text
输入
→ Prompt
→ LLM API
→ Response
→ 输出
```

当前阶段暂时不使用 LangChain 等高级框架，而是先自己实现底层流程，理解每一步具体发生了什么。

等基础功能完成后，再逐步加入 RAG、向量检索和 Agent 工作流。


## Roadmap

### v0.1 — Basic Meeting Summarization 

完成基础会议总结流程：

- [x] 使用 DeepSeek API 调用大语言模型
- [x] 使用 `.env` 管理 API Key
- [x] 将模型调用封装至 `llm.py`
- [x] 分离 System Prompt、User Instruction 与 Meeting Transcript
- [x] 支持自定义 `user_instruction`
- [x] 将会议总结结果保存为 Markdown 文件
- [x] 使用 `app.py` 作为程序入口

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
````

---

### v0.2 — Long Meeting Processing 

目标：支持较长的会议转录文本，并逐步解决上下文长度限制与会议语义连续性问题。

#### v0.2.1 — Transcript Parsing 

将原始会议转录文本解析为统一的结构化格式。

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

未来将扩展对不同 transcript 格式的识别。

---

#### v0.2.2 — Speaker-aware Chunking 

在不拆断单条发言的前提下，将结构化会议记录划分为多个 chunk。

已完成：

* [x] 实现 `chunk_messages()`
* [x] 根据文本长度控制 chunk 大小
* [x] 保证单条 speaker message 尽量保持完整
* [x] 避免 message 在 chunk 切换时丢失
* [x] 处理最后一个未满 chunk
* [x] 实现 `format_chunk()`，将结构化 message 恢复为会议文本

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

当前版本暂时使用字符数作为 chunk 大小依据。

---

#### v0.2.3 — Token-aware Chunking 

将字符长度控制升级为基于模型 Token 的长度控制。

##### v0.2.3.1 — Token Counting

* [ ] 接入 DeepSeek tokenizer
* [ ] 实现 `count_tokens()`
* [ ] 将 `max_char` 替换为 `max_tokens`
* [ ] 根据实际格式化后的 message 计算 token 数
* [ ] 保持现有 speaker-aware chunking 逻辑

目标：

```text
len(text)
    ↓
count_tokens(text)
```

使 chunk 大小与实际 LLM 上下文消耗更加一致。

##### v0.2.3.2 — Context Budget Control

在 chunk 大小之外，进一步考虑完整请求的上下文预算。

目标约束：

```text
input_tokens + reserved_output_tokens < context_limit
```

其中：

```text
input_tokens
=
system_prompt_tokens
+
instruction_tokens
+
chunk_tokens
+
message_format_overhead
```

计划实现：

* [ ] 为模型输出预留 Token
* [ ] 计算固定 Prompt 的 Token 占用
* [ ] 计算可用于 Meeting Chunk 的 Token Budget
* [ ] 加入 Safety Margin
* [ ] 避免完整请求超过模型 Context Window

预计结构：

```text
context_limit
- reserved_output_tokens
- fixed_prompt_tokens
- safety_margin
        ↓
available_chunk_tokens
```

---

#### v0.2.4 — Map-Reduce Meeting Summarization 

针对多个会议 chunk 分阶段完成总结。

##### Map

当前已完成基础版本：

* [x] 实现 `summarize_chunk()`
* [x] 实现 `summarize_chunks()`
* [x] 为每个 chunk 独立调用 LLM
* [x] 使用专用 `chunk_prompt`
* [x] 保留关键事实、建议、决定和行动项

流程：

```text
chunk 1 → summary 1
chunk 2 → summary 2
chunk 3 → summary 3
...
```

##### Reduce

计划：

* [ ] 实现 `merge_summaries()`
* [ ] 设计独立 `merge_prompt`
* [ ] 合并多个局部摘要
* [ ] 去除重复信息
* [ ] 保留跨 chunk 的讨论关系
* [ ] 生成最终会议纪要

完整流程：

```text
meeting.txt
    ↓
parse_transcript()
    ↓
messages
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

### v0.3 — Structured Output

目标：让模型输出从自由文本升级为稳定的数据结构。

计划：

* [ ] JSON structured output
* [ ] 定义 Meeting Summary Schema
* [ ] 使用 Pydantic 进行数据验证
* [ ] 结构化表示：

  * Topics
  * Decisions
  * Action Items
  * Participants
  * Open Questions
* [ ] 处理格式错误与模型输出异常

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

### v0.4 — Retrieval-Augmented Generation (RAG)

目标：让会议助手能够利用外部知识库辅助理解会议内容。

计划：

* [ ] 学习 Embedding
* [ ] 使用 NumPy 实现 Cosine Similarity
* [ ] 实现 Top-K Retrieval
* [ ] 构建最小可用 RAG Pipeline
* [ ] 使用 FAISS 管理向量索引
* [ ] 支持会议相关术语、项目背景与历史会议检索

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

### v0.5 — Meeting Agent Workflow

目标：从“会议总结工具”进一步发展为完整 Meeting Agent。

计划加入：

* [ ] Meeting Summary
* [ ] Research Progress Extraction
* [ ] Action Item Extraction
* [ ] Meeting Email Generation
* [ ] Fact Checking
* [ ] Historical Meeting Retrieval
* [ ] Multi-step Workflow
* [ ] Error Handling & Logging

可能的完整流程：

```text
Transcript
    ↓
Parse
    ↓
Chunk
    ↓
Summarize
    ↓
Merge
    ↓
Fact Check
    ↓
Structured Meeting Data
    ↓
Email / Report / Query
```

---

### Future

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
* 长文本处理
* Embedding
* 向量检索
* Retrieval-Augmented Generation（RAG）
* LLM Agent

项目早期会尽量避免直接使用高级框架封装核心流程，希望先理解这些技术底层到底是如何工作的。

## License

本项目目前主要用于个人学习与实验。


