from .schemas import MeetingSummary
import json
from pydantic import ValidationError
from .llm import call_llm

def call_llm_structured(
    system_prompt: str,
    user_prompt: str,
    schema =  MeetingSummary,
    max_retries: int = 2
) -> MeetingSummary:##返回类型没改
    
    result = call_llm(system_prompt,user_prompt)
    
    try:
        parsed_result = json.loads(result)
    except json.JSONDecodeError as e:
        if max_retries <= 0:
            raise
        else:
            retry_user_prompt = user_prompt + f'''\n
[原输出]
{result}

[错误原因]
{e}

[请重新按要求生成]
'''
            ##test
            ##print('JSON failed, retrying...')
            
            return call_llm_structured(
                system_prompt=system_prompt,
                user_prompt=retry_user_prompt,
                schema=schema,
                max_retries= max_retries-1
                )
    try:
        validated_result = schema(**parsed_result)
    except ValidationError as e:
        if max_retries <= 0:
            raise
        else:
            retry_user_prompt = user_prompt + f'''\n
[原输出]
{parsed_result}
            
[错误原因]
{e}
            
[请重新按要求生成]
'''
            ##test
            ##print('Validation failed, retrying...')
            return call_llm_structured(
                system_prompt=system_prompt,
                user_prompt=retry_user_prompt,
                schema=schema,
                max_retries= max_retries-1
                )
    return validated_result
    
    