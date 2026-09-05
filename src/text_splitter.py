from .token_utils import count_tokens

##chunk messages
def chunk_messages(messages: list[dict],
                   max_tokens: int = 4000
                   ) -> list[list[dict]]:
    chunks = []
    chunk = []
    chunk_token_count = 0
    for message in messages:
        formatted_message = f"{message['speaker']}({message['timestamp']}): {message['content']}\n"
        message_token_count = count_tokens(formatted_message)
        
        if chunk_token_count + message_token_count <= max_tokens:
            chunk_token_count += message_token_count
            chunk.append(message)
        else:
            if chunk:
                chunks.append(chunk)
            chunk = [message]
            chunk_token_count = message_token_count
    if chunk:
        chunks.append(chunk)
    return chunks
        
##把chunk文本化
def format_chunk(chunk: list[dict]) -> str:
    formatted_messages = []
    for message in chunk:
        formatted_message = f"{message['speaker']}({message['timestamp']}): {message['content']}\n"
        formatted_messages.append(formatted_message)
    return ''.join(formatted_messages)
