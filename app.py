from src import save_result,summarize_long_meeting
from pathlib import Path

def main() -> None:
   result = summarize_long_meeting(
      meeting_txt_path='data/test.txt',
      system_prompt_path='prompts/system_prompt.txt',
      chunk_prompt_path='prompts/chunk_prompt.txt'
      )
   print(result)
   
   
if __name__ == '__main__':
    main() 