from src import save_result,summarize_long_meeting,send_message,create_session
from pathlib import Path
from src.database import Base,engine

def main() -> None:
   meeting_text = """
    张三：我们下周需要完成项目第一版。
    李四：我负责整理数据。
    王五：我负责模型训练。
    张三：那就定在下周五之前完成初版，周四晚上先内部检查一次。
    """
   result = summarize_long_meeting()

   print(result)

   

   
   
if __name__ == '__main__':
    main() 