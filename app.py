from src import save_result,summarize_long_meeting,send_message,create_session
from pathlib import Path
from src.database import Base,engine

def main() -> None:
   system_prompt = '''你是一个简洁、可靠的聊天助手。

请遵守以下规则：
1. 认真参考当前对话中已经提供的历史消息。
2. 如果用户的问题涉及前文内容，应根据历史消息回答，不要假装不知道。
3. 不要编造历史中没有出现的信息。
4. 回答尽量简洁、直接。'''
   
   Base.metadata.create_all(bind=engine)
   

   user_input = input('Input: ')
   result = send_message(
            system_prompt=system_prompt,
            session_id=1,
            user_input=user_input,
            history_turns=5
         )
   print(result)
   
   

   
   
if __name__ == '__main__':
    main() 