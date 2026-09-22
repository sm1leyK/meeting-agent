

def build_context(results: list[tuple[str,float]]) -> str:
    context = ''
    for num, result in enumerate(results,start=1):
        context += f'[Context {num}]: {result[0]}\n'
    return context