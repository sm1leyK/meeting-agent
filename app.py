from src import summarize_meeting,save_result

def main() -> None:
   result = summarize_meeting()
   save_result(result)
   print(result)
   
if __name__ == '__main__':
    main() 