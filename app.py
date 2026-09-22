from src import save_result,summarize_long_meeting,send_message,create_session
from pathlib import Path



from src.rag.chunking import split_document
from src.rag.embedding import embed_chunks
from src.rag.vector_store import VectorStore
from src.rag.rag import answer_with_rag


def test_rag_end_to_end():
    document = """
项目组今天讨论了 RAG 模块的开发计划。

K 负责实现向量检索模块，并在本周五前完成。

数据库迁移计划安排在下周一进行。

项目还需要补充更多测试用例。
"""

    # M1: chunking
    chunks = split_document(
        document,
        max_tokens=20,
        overlap=10
    )

    print("Chunks:")
    for i, chunk in enumerate(chunks, start=1):
        print(f"{i}. {chunk}")

    # M2: embedding
    embeddings = embed_chunks(chunks)

    # M3: vector store
    store = VectorStore()
    store.add(chunks, embeddings)

    # M4-M7: query -> retrieval -> context -> LLM
    query = "K这周负责做什么？"

    answer = answer_with_rag(
        query=query,
        store=store,
        top_k=2
    )

    print("\nQuestion:")
    print(query)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    test_rag_end_to_end()