from ..core.token_utils import count_tokens,split_by_tokens
import re

def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.?!。？！])',text)
    return [sentence for sentence in sentences if sentence]
    
    

def split_document(
    text: str,
    max_tokens: int = 400,
    overlap: int = 50
) -> list[str]:

    chunks = []
    cur_lines = []
    cur_tokens = 0

    sentences = split_into_sentences(text)

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        
        if sentence_tokens > max_tokens:
            pieces = split_by_tokens(sentence, max_tokens)
        else:
            pieces = [sentence]

        for piece in pieces:
            piece_tokens = count_tokens(piece)

            if cur_tokens + piece_tokens <= max_tokens:
                cur_lines.append(piece)
                cur_tokens += piece_tokens
                continue

            if cur_lines:
                chunks.append("".join(cur_lines))

            overlap_lines = []
            overlap_tokens = 0

            for old_line in reversed(cur_lines):
                old_line_tokens = count_tokens(old_line)

                if overlap_tokens + old_line_tokens > overlap:
                    break

                overlap_lines.append(old_line)
                overlap_tokens += old_line_tokens

            overlap_lines.reverse()

            cur_lines = overlap_lines
            cur_tokens = overlap_tokens

            cur_lines.append(piece)
            cur_tokens += piece_tokens

    if cur_lines:
        chunks.append("".join(cur_lines))

    return chunks

