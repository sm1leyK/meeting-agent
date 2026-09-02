
##chunk messages
def chunk_messages(messages: list[dict],
                   max_char: int = 2000
                   ) -> list[list[dict]]:
    chunks = []
    chunk = []
    chunk_char_count = 0
    for message in messages:
        message_char_count = (len(message['speaker']) 
        + len(message['timestamp'])
        + len(message['content']))
        if chunk_char_count + message_char_count <= max_char:
            chunk_char_count += message_char_count
            chunk.append(message)
        else:
            if chunk:
                chunks.append(chunk)
            chunk = [message]
            chunk_char_count = message_char_count
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

