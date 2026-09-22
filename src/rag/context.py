

def build_context(chunks: list[str]) -> str:
    result = ''
    for num, chunk in enumerate(chunks,start=1):
        result += f'[Context {num}]: {chunk}\n'
    return result