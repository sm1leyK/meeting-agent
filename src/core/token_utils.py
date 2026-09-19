from tokenizers import Tokenizer
from pathlib import Path


base_dir = Path(__file__).parent.parent.parent
chat_tokenizer_dir = base_dir / 'tokenizers'
tokenizer_dir = chat_tokenizer_dir / 'tokenizer.json'
tokenizer = Tokenizer.from_file(str(tokenizer_dir))



def count_tokens(text: str) -> int:
        result = tokenizer.encode(text)
        return len(result)

def split_by_tokens(text: str,max_tokens: int = 400) -> list[str]:
        encoded_ids = tokenizer.encode(text).ids
        chunked_text = []
        chunk_list = [encoded_ids[i:i+max_tokens] for i in range(0,len(encoded_ids),max_tokens)]
        for chunk in chunk_list:
                decoded_text = tokenizer.decode(chunk)
                chunked_text.append(decoded_text)
        return chunked_text
        

def calculate_token_budget(
        prompt_tokens: int,
        context_limit: int = 1000000,
        reserved_output_tokens: int = 4000,
        safety_margin: int = 1000,
        preferred_limit: int = 8000
        ) -> int:
        available_chunk_tokens = (
                context_limit 
                - prompt_tokens 
                - reserved_output_tokens
                - safety_margin
                )
        if available_chunk_tokens <= 0:
                raise ValueError('当前 Prompt + 输出预算已经超过模型上下文限制')
        effective_chunk_limit = min(available_chunk_tokens,preferred_limit)
        return effective_chunk_limit

chunks = split_by_tokens('hello, my name is sm1leyK.',4)
print(chunks)