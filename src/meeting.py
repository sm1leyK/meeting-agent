from .llm import call_llm
from pathlib import Path
import os
from .text_splitter import format_chunk,chunk_messages
from .io_utils import load_txt,save_result
from .token_utils import count_tokens,calculate_token_budget
from .transcript_parser import parse_transcript



##读取并生成用户提示词
def build_user_prompt(
    meeting_txt: str,
    user_instruction = '请生成结构化会议纪要，包含：会议主题、主要讨论、当前问题、明确决定、后续行动。'
) -> str:
    user_prompt = f'''
你将收到两部分内容：

【用户任务】
{user_instruction}

【会议原文】
{meeting_txt}

请严格按照用户任务处理会议原文。

要求：

1. 所有结论必须基于会议原文，不得补充原文中不存在的信息。
2. 如果原文中没有明确说明某项信息，请标记为“未明确”或直接说明无法确定。
3. 区分以下信息类型，不要混淆：
   - 已发生的事实
   - 个人观点或建议
   - 初步讨论方向
   - 明确决定
4. 如果不同参会者观点存在冲突，应保留不同观点，不要擅自判断哪一方正确。
5. 对人物、时间、数字、模型名称、专业术语等信息尽量保持原文准确。
6. 不要因为用户要求输出完整而自行推测缺失内容。
7. 优先满足【用户任务】中的具体要求，包括输出内容、长度、语言和格式。
8. 如果用户任务与会议原文中的信息不足以完成任务，请明确指出缺失的信息。
9. 删除无意义的口语重复、停顿和语气词，但不要改变原意。
10. 输出内容应清晰、结构化、便于阅读。

请先完整理解会议原文，再根据【用户任务】生成最终结果。
'''
    return user_prompt

##调用llm
def summarize_meeting(
    user_instruction_path: Path | None = None,
    meeting_txt_path = Path(__file__).parent.parent / 'data' / 'meeting.txt',
    system_prompt_path = Path(__file__).parent.parent / 'prompts' / 'system_prompt.txt'
                      ) -> str:
    system_prompt = load_txt(system_prompt_path)
    meeting_txt = load_txt(meeting_txt_path)
    if user_instruction_path and user_instruction_path.exists():
        user_instruction = load_txt(user_instruction_path)
        user_prompt = build_user_prompt(meeting_txt,user_instruction)
    else:
        user_prompt = build_user_prompt(meeting_txt)
    
    result = call_llm(system_prompt,user_prompt)
    return result

##构造局部prompt
def summarize_chunk(
    chunk_text: str,
    chunk_prompt_path: Path,
    system_prompt_path: Path
    ) -> str:
    
    chunk_prompt = load_txt(chunk_prompt_path)
    system_prompt = load_txt(system_prompt_path)
    user_prompt = f'''
{chunk_prompt}
    
[当前会议片段]
    
{chunk_text}
'''
    summary = call_llm(system_prompt,user_prompt)
    return summary

##总结局部prompt
def summarize_chunks(
    chunks: list[list[dict]],
    chunk_prompt_path: Path,
    system_prompt_path: Path
    ) -> list[str]:
    summaries = []
    
    for chunk in chunks:
        chunk_text = format_chunk(chunk)
        summary = summarize_chunk(chunk_text,chunk_prompt_path,system_prompt_path)
        summaries.append(summary)
    
    return summaries

##准备 chunk budget
def prepare_chunk_budget(
    system_prompt_path: Path = Path(__file__).parent.parent / 'prompts' / 'system_prompt.txt',
    chunk_prompt_path: Path = Path(__file__).parent.parent / 'prompts' / 'chunk_prompt.txt',
    context_limit: int = 1000000,
    reserved_output_tokens: int = 4000,
    safety_margin: int = 1000,
    preferred_chunk_limit: int = 8000
    ) -> int:
    ##计算system和chunk prompt
    system_prompt_tokens = count_tokens(load_txt(system_prompt_path))
    chunk_prompt_tokens = count_tokens(load_txt(chunk_prompt_path))
    fixed_prompt_tokens = system_prompt_tokens + chunk_prompt_tokens
    effective_chunk_limit = calculate_token_budget(fixed_prompt_tokens,context_limit,reserved_output_tokens,safety_margin,preferred_chunk_limit)
    return effective_chunk_limit

##调度
def summarize_long_meeting(
    meeting_txt_path = Path(__file__).parent.parent / 'data' / 'meeting.txt',
    system_prompt_path: Path = Path(__file__).parent.parent / 'prompts' / 'system_prompt.txt',
    chunk_prompt_path: Path = Path(__file__).parent.parent / 'prompts' / 'chunk_prompt.txt',
    context_limit: int = 1000000,
    reserved_output_tokens: int = 4000,
    safety_margin: int = 1000,
    preferred_chunk_limit: int = 8000
) -> list[str]:
    ##获取会议内容+格式化
    meeting_txt = load_txt(meeting_txt_path)
    messages = parse_transcript(meeting_txt)
    
    ##获取token限制
    effective_chunk_limit = prepare_chunk_budget(
        system_prompt_path=system_prompt_path,
        chunk_prompt_path=chunk_prompt_path,
        context_limit=context_limit,
        reserved_output_tokens=reserved_output_tokens,
        safety_margin=safety_margin,
        preferred_chunk_limit=preferred_chunk_limit
        )
    
    ##获取chunks
    chunks = chunk_messages(messages=messages,max_tokens=effective_chunk_limit)
    ##获取summaries
    #summaries = summarize_chunks(chunks=chunks,chunk_prompt_path=chunk_prompt_path,system_prompt_path=system_prompt_path)
    #return summaries
    
    ##test
