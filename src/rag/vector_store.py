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
    