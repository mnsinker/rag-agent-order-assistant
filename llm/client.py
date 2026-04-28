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
def call_llm(query: str, tool_schemas: list):
    prompt = f'''
    你是一个AI助手，负责理解用户意图, 并提取必要参数。

    用户问题:
    {query}
    
    任务: 
    1. 判断用户的意图 (intent)
    2. 提取必要参数 (例如 order_id)
    
    可用意图 (intent):
    - risk_check (判断订单风险)
    - check_refund (查询是否可退款)
    - get_shipping_status (查询物流) 
    
    规则: 
    - intent 必须从上面列表中选择一个
    - order_id 如果存在, 必须提取
    - 不允许遗漏关键参数
    
    输出要求：
    1. 只返回JSON, 格式如下：
    {{"intent": "intent_name", "args": {{"order_id": "123"}}}}    
    '''

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )

    return response.choices[0].message.content


# 3. call llm with retry
def call_llm_with_retry(query: str, tool_schemas: list, error_message):
    prompt = f'''
                用户问题:
                {query}
                
                你的错误是: 
                {error_message}
                        
                请修正以下问题:  
                1. intent 必须是以下之一: 
                - risk_check
                - check_refund
                - get_shipping_status
                
                2. 必须提取必要参数 (如 order_id)
                3. 必须返回合法 json, 格式如下:
                {{"intent": "intent_name", "args": {{"order_id": "123"}}}}
            '''

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )

    return response.choices[0].message.content


