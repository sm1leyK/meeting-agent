from .llm import call_llm
from .storage import load_history,save_message

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
    history_turns: int=5,
    ) -> str:
    
    history = load_history(session_id=session_id)
    
    messages = build_chat_messages(
        system_prompt=system_prompt,
        history=history,
        user_input=user_input,
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