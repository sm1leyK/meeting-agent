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

def main() -> None:
   test_split_document()

   

   
   
if __name__ == '__main__':
    main() 