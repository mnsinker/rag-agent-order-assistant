import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# 1. 创建client对象
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url='https://api.deepseek.com'
)


# 2. call llm
def call_llm(query: str, tool_schemas: list) -> list:
    prompt = f'''
    你是一个AI助手，可以根据用户问题选择合适的工具, 并提取必要参数。

    用户问题:
    {query}
    
    可用工具:
    {tool_schemas}
    
    任务: 
    1. 选择正确的工具
    2. 从用户问题中提取参数 (尤其是 order_id)
    
    规则: 
    - order_id 一定要从用户问题中提取
    - 例如: 
        - "订单123" → order_id = "123"
        - "查询订单456状态" → order_id = "456"
    - 不允许遗漏关键参数
    
    输出要求：
    1. 只返回JSON
    格式如下：
    {{
      "steps": [
        {{"tool": "tool_name", "args": {...}}}
      ]
    }}
    '''

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )

    content = response.choices[0].message.content


    return content


# 3. call llm with retry
def call_llm_with_retry(query: str, tool_schemas: list, error_message):
    prompt = f'''
                用户问题:
                {query}
                
                可用工具:
                {tool_schemas}
                
                你的错误是: 
                {error_message}
                
                请修正以下问题:  
                - 确保所有必要参数都被正确提取 (如 order_id)
                - 不允许 args 为空
                - 必须返回合法 json
            '''

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    return content


