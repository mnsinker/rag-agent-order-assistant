from openai import OpenAI
from config.secrets import get_secret


api_key = get_secret("DEEPSEEK_API_KEY")
base_url = get_secret("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


client = OpenAI(api_key=api_key, base_url=base_url)


def build_intent_prompt(query: str) -> str:
    return f"""
你是一个AI助手，负责理解用户意图，并提取必要参数。

用户问题:
{query}

任务:
1. 判断用户的意图 intent
2. 提取必要参数，例如 order_id

可用意图 intent:
- risk_check: 判断订单风险
- check_refund: 查询是否可退款
- get_shipping_status: 查询物流
- decide_coupon: 判断是否可发优惠券

规则:
- intent 必须从上面列表中选择一个
- order_id 如果存在，必须提取
- 不允许遗漏关键参数

输出要求:
只返回 JSON，格式如下：
{{"intent": "intent_name", "args": {{"order_id": "123"}}}}
"""


def call_llm(query: str, tool_schemas: list):
    prompt = build_intent_prompt(query)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content


def call_llm_with_retry(query: str, tool_schemas: list, error_message):
    prompt = f"""
用户问题:
{query}

你的错误是:
{error_message}

请修正以下问题:
1. intent 必须是以下之一:
- risk_check
- check_refund
- get_shipping_status
- decide_coupon

2. 必须提取必要参数，例如 order_id
3. 必须返回合法 JSON，格式如下:
{{"intent": "intent_name", "args": {{"order_id": "123"}}}}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content