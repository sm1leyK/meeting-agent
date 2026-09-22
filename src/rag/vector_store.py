import numpy as np

class VectorStore:
    chunks: list[str]
    embeddings: np.ndarray | None
    
    def __init__(self):
        self.chunks = [] 
        self.embeddings = None
        
    def add(self, chunks: list[str], embeddings: np.ndarray) -> None:
        if len(chunks) != embeddings.shape[0]:
            raise ValueError("Number of chunks must match number of embeddings.")
        
        self.chunks.extend(chunks)
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.concatenate([self.embeddings,embeddings],axis=0)
        
    def get_all(self) -> tuple[list[str],np.ndarray | None]:
        return (self.chunks,self.embeddings)
    
    def search(self, query_vector: np.ndarray, top_k: int) -> list[tuple[str,float]]:
        
        similarities = (np.dot(self.embeddings,query_vector) / 
                        (np.linalg.norm(query_vector) * np.linalg.norm(self.embeddings,axis=1))
                        )
        indices = np.argsort(similarities)[::-1][:top_k]
        
        return [
            (self.chunks[i], float(similarities[i]))
            for i in indices
        ]
        