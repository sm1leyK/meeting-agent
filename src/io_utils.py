from pathlib import Path

##读取文本
def load_txt(path: str) -> str:
    try:
        with open(path,'r') as file:
            txt = file.read()
        return txt
    except FileNotFoundError as e:
        raise FileNotFoundError(f'file not found: {e}')
    
##保存结果
def save_result(result: str,
                output_path = Path(__file__).parent.parent / 'outputs' / 'test_result.md'
                ) -> None:
    try:
        with open(output_path,'w') as file:
            file.write(result)
        print(f'输出结果保存成功。 位置：{output_path}')
    except FileNotFoundError as e:
        raise FileNotFoundError(f'file not found: {e}')