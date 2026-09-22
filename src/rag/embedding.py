from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def embed_text(text: str) -> np.ndarray:
    return model.encode(text)
    

def embed_chunks(chunks: list[str]) -> np.ndarray:
    return model.encode(chunks)

