from .client import client
def generate_final_result(query: str, tool_results_str: list) -> str:
    prompt = f'''
    用户原始问题: 
    {query}

    工具执行结果: 
    {tool_results_str}

    请基于工具执行结果回答用户问题. 
    要求: 
    1. 不要编造信息
    2. 只基于工具结果回答
    3. 简洁清晰
    '''

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[{'role': 'user', 'content': prompt}],
    )

    return response.choices[0].message.content