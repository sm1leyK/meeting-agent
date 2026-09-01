# Meeting Agent

一个轻量级的 Python 会议助手，使用大语言模型根据会议记录生成结构化会议纪要。

这个项目目前主要作为一个 LLM 应用开发学习项目，用来从底层理解 Prompt 设计、API 调用、会议文本处理，以及后续的 RAG 检索问答等内容。

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

### v0.1 基础会议摘要

* [x] Python 虚拟环境
* [x] `.env` 环境变量配置
* [x] DeepSeek API 调用
* [x] 会议文本读取
* [x] System Prompt 读取
* [x] 自定义用户任务
* [x] 结构化会议纪要生成
* [x] 将会议纪要保存为 Markdown 文件

### v0.2 长文本处理

* [ ] 文本切块
* [ ] Token 长度处理
* [ ] Map-Reduce 摘要

### v0.3 结构化输出

* [ ] JSON 输出
* [ ] Pydantic 数据验证
* [ ] 行动项结构化提取

### v0.4 RAG

* [ ] Embedding
* [ ] Cosine Similarity
* [ ] Top-K 检索
* [ ] 基于会议内容的问答

### v0.5 向量检索

* [ ] FAISS
* [ ] 向量索引保存与读取

### v0.6 Meeting Agent

* [ ] 科研邮件生成
* [ ] 会议纪要事实核查
* [ ] Agent 工作流

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


