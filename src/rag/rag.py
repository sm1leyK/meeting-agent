from .embedding import embed_text
from .context import build_context
from .vector_store import VectorStore 
from ..core.llm import call_llm,build_basic_messages

def answer_with_rag(
    query: str,
    store: VectorStore,
    top_k: int
    ) -> str:
    
    query_vector = embed_text(text=query)
    
    chunks = store.search(query_vector=query_vector, top_k=top_k)
    
    context = build_context(chunks=chunks)
    
    system_prompt = '''你是一个基于提供上下文回答问题的助手。
只能根据提供的上下文回答。
如果上下文里没有答案，就明确说不知道，不要编造。'''

    user_message = f'''
Context:
{context}

Question:
{query}
'''

    messages = build_basic_messages(system_prompt=system_prompt,user_prompt=user_message)
    result = call_llm(messages=messages)
    return result
    
def should_use_rag(
    best_score,
    threshold: float=0.25
) -> bool:
    
    if best_score > threshold:
        return True
    
    return False

    