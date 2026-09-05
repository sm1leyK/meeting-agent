import re

##文本的格式化
def parse_transcript(text: str) -> list:
    
    ## speaker(timestamp): content
    messages = []
    pattern = r"^(.*?)\((\d{2}:\d{2}:\d{2})\):\s*(.*)$"
    lines = text.splitlines()
    for line in lines:
        match = re.match(pattern,line)
        message = {}
        if match:
            message['speaker'] = match.group(1)
            message['timestamp'] = match.group(2)
            message['content'] = match.group(3)
            messages.append(message)
        ##不match的内容还没考虑
    return messages    
    
    

        
    

        