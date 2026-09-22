from pathlib import Path

from src.database import Base, engine
from src.io_utils import load_txt
from src.meeting.meeting import summarize_long_meeting
from src.rag import split_document, embed_chunks, VectorStore
from src.chat.chat import send_message
from src.chat.storage import create_session


BASE_DIR = Path(__file__).parent
MEETING_PATH = BASE_DIR / "data" / "meeting.txt"


def build_rag_store(document_path: str) -> VectorStore:
    document = load_txt(document_path)

    chunks = split_document(
        text=document,
        max_tokens=400,
        overlap=50
    )

    embeddings = embed_chunks(chunks)

    store = VectorStore()
    store.add(chunks, embeddings)

    return store


def summarize_meeting():
    summary = summarize_long_meeting(
        meeting_txt_path=str(MEETING_PATH)
    )

    print("\n===== Meeting Summary =====")
    print(summary)
    print()


def chat_with_meeting():
    store = build_rag_store(str(MEETING_PATH))

    session_id = create_session("Meeting RAG Chat")

    system_prompt = """
你是一个有帮助的会议助手。
可以回答用户的一般问题，也可以根据会议知识库中的内容回答会议相关问题。
"""

    print("\n进入会议聊天模式，输入 exit 返回主菜单。\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        answer = send_message(
            system_prompt=system_prompt,
            session_id=session_id,
            user_input=user_input,
            store=store,
            top_k=3,
            threshold=0.25
        )

        print(f"\nAssistant: {answer}\n")


def main():
    Base.metadata.create_all(bind=engine)

    while True:
        print("===== Meeting Agent =====")
        print("1. Summarize meeting")
        print("2. Chat with meeting")
        print("3. Exit")

        choice = input("\n请选择: ").strip()

        if choice == "1":
            summarize_meeting()

        elif choice == "2":
            chat_with_meeting()

        elif choice == "3":
            print("Bye.")
            break

        else:
            print("无效选项，请重新输入。\n")


if __name__ == "__main__":
    main()