from ..core.llm import call_llm
from .storage import load_history,save_message
from ..rag import VectorStore,embed_text,should_use_rag,answer_with_rag,build_context

def build_chat_messages(
    system_prompt: str,
    history: list[dict],
    user_input: str,
    history_turns: int=5
    ) -> list[dict]:
    
    return [
        {'role':'system','content':system_prompt},
            
        *[{'role':m['role'],'content':m['content']} for m in history[-history_turns*2:]],
        
        {'role':'user','content':user_input}
    ]
    
def send_message(
    system_prompt: str,
    session_id: int,
    user_input: str,
    store: VectorStore | None=None,
    top_k: int=5,
    history_turns: int=5,
    threshold: float=0.25
    ) -> str:
    
    history = load_history(session_id=session_id)
    
    user_message = user_input
    effective_system_prompt = system_prompt
    
    if store is not None:
        query_vector = embed_text(user_input)
        results = store.search(
                        query_vector=query_vector,
                        top_k=top_k
                    )
        if results is None:
            raise ValueError('Store is empty.')
        
        if should_use_rag(threshold=threshold,best_score=results[0][1]):
            
            context = build_context(results=results)

            effective_system_prompt = system_prompt + """
当用户消息中包含 Context 时：
- 仅根据提供的 Context 回答问题。
- 不要使用 Context 之外的信息补充事实。
- 如果 Context 无法回答问题，请明确说明无法从提供的信息中得到答案。
"""
            
            user_message = f'''
            Context:
            {context}
            
            Question:
            {user_input}
            '''
    
    messages = build_chat_messages(
        system_prompt=effective_system_prompt,
        history=history,
        user_input=user_message,
        history_turns=history_turns
        )
    
    save_message(
            session_id=session_id,
            role='user',
            content=user_input    
        )
    
    result = call_llm(messages=messages)
    
    save_message(
        session_id=session_id,
        role='assistant',
        content=result
    )
    
    return result