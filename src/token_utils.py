import transformers
from pathlib import Path

def count_tokens(text: str) -> int:
        base_dir = Path(__file__).parent.parent
        chat_tokenizer_dir = base_dir / 'tokenizers'

        tokenizer = transformers.AutoTokenizer.from_pretrained( 
        chat_tokenizer_dir, trust_remote_code=True
        )

        result = tokenizer.encode(text)
        return len(result)