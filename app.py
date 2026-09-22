from src import save_result,summarize_long_meeting,send_message,create_session
from pathlib import Path
from src.rag.chunking import split_document
from src.core.token_utils import count_tokens

def test_split_document():
    text = (
        "第一行内容。\n"
        "第二行内容。\n"
        "第三行内容。\n"
        "第四行内容。\n"
        "第五行内容。\n"
    )

    chunks = split_document(
        text,
        max_tokens=12,
        overlap=4
    )

    print(f"chunk 数量: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks, start=1):
        print(f"===== Chunk {i} =====")
        print(chunk)
        print(f"tokens: {count_tokens(chunk)}")
        print()



from src.rag.embedding import embed_chunks, embed_text
from src.rag.vector_store import VectorStore


def test_vector_search():
    chunks = [
        "K负责实现RAG模块，并在周五前完成。",
        "会议决定下周进行数据库迁移。",
        "大家讨论了国庆假期的旅行安排。",
        "项目需要补充更多测试用例。"
    ]

    embeddings = embed_chunks(chunks)

    store = VectorStore()
    store.add(chunks, embeddings)

    query = "什么时候进行数据库迁移？"
    query_vector = embed_text(query)

    results = store.search(query_vector, top_k=2)

    print("Query:")
    print(query)

    print("\nTop results:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result}")


if __name__ == "__main__":
    test_vector_search()

