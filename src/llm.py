from .config import Config
from openai import OpenAI

def call_llm(system_prompt: str, user_prompt: str) -> str:
    ##设置client
    config = Config()
    try:
        config.validate()
    except ValueError as e:
        print(e)
        exit()
    client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url='https://api.deepseek.com'
    )

    ##回复
    response = client.chat.completions.create(
    model='deepseek-v4-flash',
    messages=[
        {'role':'system','content':system_prompt},
        {'role':'user','content':user_prompt}
    ],
    stream=False,
    ##reasoning_effort='high',
    ##extra_body={'thinking':{'type':'enabled'}}
    )

    response_text = response.choices[0].message.content
    return response_text
