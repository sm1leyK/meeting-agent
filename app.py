from src import save_result,summarize_long_meeting,send_message,create_session
from pathlib import Path



from src.rag.embedding import embed_chunks
from src.rag.vector_store import VectorStore
from src.chat.chat import send_message
from src.chat.storage import create_session


def test_chat_rag_router():
    chunks = [
        "K负责实现RAG模块，并在本周五前完成。",
        "数据库迁移计划安排在下周一进行。",
        "项目还需要补充更多测试用例。"
    ]

    embeddings = embed_chunks(chunks)

    store = VectorStore()
    store.add(chunks, embeddings)

    session_id = create_session("RAG Router Test")

    system_prompt = "你是一个有帮助的聊天助手。"

    queries = [
        "K这周负责什么？",
        "什么是决策树？"
    ]

    for query in queries:
        print("=" * 50)
        print("User:", query)

        answer = send_message(
            system_prompt=system_prompt,
            session_id=session_id,
            user_input=query,
            store=store,
            top_k=2,
            threshold=0.25
        )

        print("Assistant:", answer)


if __name__ == "__main__":
    test_chat_rag_router()