import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# 创建client对象
client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
def call_llm(query: str, tool_schemas: list) -> list:
    prompt = f'''
    你是一个AI助手，可以根据用户问题选择合适的工具。

    用户问题:
    {query}
    
    可用工具:
    {tool_schemas}
    
    请根据用户问题，选择合适的工具，并返回调用步骤。
    
    要求：
    1. 只返回JSON
    2. 格式如下：
    {{
      "steps": [
        {{"tool": "tool_name", "args": {...}}}
      ]
    }}
    '''

    response = client.chat.completions.create(
        model='qwen-plus',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    print(f'[LLM RAW] {content}, \n[TYPE] {type(content)}')

    return content