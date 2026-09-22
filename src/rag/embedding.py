from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def embed_text(text: str) -> np.ndarray:
    return model.encode(text)
    

def embed_chunks(chunks: list[str]) -> np.ndarray:
    return model.encode(chunks)

texts = [
    "今天讨论RAG。",
    "明天去健身。",
    "K负责实现检索模块。"
]

vectors = embed_chunks(texts)

print(vectors.shape)