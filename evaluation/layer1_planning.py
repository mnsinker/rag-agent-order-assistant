from agents.agent import decide_with_retry
from tools.get_all_tool_schemas import get_all_tool_schemas

cases = [
    {
        "query": "订单123能退款吗",
        "expected_tools": ["check_refund"],
        "expected_args": {"check_refund": ["order_id"]}
     },
    {
        "query": "订单123能退款吗, 顺便看看物流",
        "expected_tools": ["check_refund", "get_shipping_status"],
        "expected_args": {"get_shipping_status": ["order_id"]}
    },
    {
        "query": "订单123能退款的话 帮我直接退款",
        "expected_tools": ["check_refund", "create_refund"],
        "expected_args": {"check_refund": ["order_id"], "create_refund": ["order_id"]}
    },
    {
        "query": "订单999能退款吗",
        "expected_tools": ["check_refund"],
        "expected_args": {"check_refund": ["order_id"]}
    },
    {
        "query": "user u1 的订单123 有没有风险",
        "expected_tools": ["risk_check"],
        "expected_args": {"get_order": ["order_id"]}
    },
]


def get_tool_calls(cases: list) -> list:
    tool_calls_with_query = []
    for case in cases:
        # 1. 拿到 query
        query = case["query"]
        # 2. 拿到schemas + call llm
        tool_schemas = get_all_tool_schemas()
        tool_call = decide_with_retry(query, tool_schemas, max_retry=2)
        # 3. append tool call
        tool_calls_with_query.append({
            "query": query,
            "tool_call": tool_call,
        })
    return tool_calls_with_query


def evaluate(cases: list, tool_calls_with_query: list):
    '''
    compare expected vs actual, and record results.
    '''
    results = []
    all_tools = []
    all_llm_args = []
    all_dep_args = []
    len_cases = len(cases)
    for case in cases:
        # 0. define
        query = case["query"]
        expected_tools = case["expected_tools"]
        expected_args = case["expected_args"]

        steps = None
        for tc in tool_calls_with_query:
            if tc["query"] == query:
                steps = tc.get("tool_call", {}).get("steps", None)
                break

        if not steps:
            print(f"[ERROR] query {query} not found in tool list")

        # 1. 验证 actual_tools (允许多, 但只要包含expected 就ok; 是否多包含了错的, 需要人工判断)
        actual_tools = [step["tool"] for step in steps]
        correctness_tools = all(et in actual_tools for et in expected_tools)

        # 2. 验证 args
        correctness_llm_args = True
        correctness_dep_args = True  # 不含 dataclass

        for step in steps:
            step_tool = step["tool"]
            step_args = step["args"]

            # 2.1 必须包含 expected primitive
            if step_tool in expected_args:
                for arg in expected_args[step_tool]:
                    if arg not in step_args:
                        correctness_llm_args = False
            # 2.2 不能有 dataclass (简单判断)
            for v in step_args.values():
                if not isinstance(v, (str, int, float, bool, type(None))):
                    correctness_llm_args = False

        # 3. append result
        all_tools.append(correctness_tools)
        all_llm_args.append(correctness_llm_args)
        all_dep_args.append(correctness_dep_args)
        results.append({
            "query": query,
            "correctness_tools": correctness_tools,
            "correctness_llm_args": correctness_llm_args,
            "correctness_dep_args": correctness_dep_args,
        })

    return results, len_cases, sum(all_tools), sum(all_llm_args), sum(all_dep_args)



if __name__ == '__main__':
    # 1. get tool_calls
    # tool_calls_with_query = cases_call_llm(cases_planning)
    tool_calls_with_query = [
        {'query': '订单123能退款吗',
         'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}}]}},

        {'query': '订单123能退款吗, 顺便看看物流',
         'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}},
                                 {'tool': 'get_shipping_status', 'args': {'order_id': '123'}}]}},

        {'query': '订单123能退款的话 帮我直接退款',
         'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}},
                                 {'tool': 'create_refund', 'args': {'order_id': '123'}}]}},

        {'query': '订单999能退款吗',
         'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '999'}}]}},

        {'query': 'user u1 的订单123 有没有风险',
         'tool_call': {'steps': [{'tool': 'risk_check', 'args': {}}]}}]

    # 2. get test results
    results, len_cases, correct_tools, correct_llm_args, correct_dep_args = evaluate(cases, tool_calls_with_query)
    print(f'tool_calls_with_query: {tool_calls_with_query}')
    print(f'results: {results}')
    print(f'len_cases: {len_cases}')
    print(f'correct_tools: {correct_tools}')
    print(f'correct_llm_args: {correct_llm_args}')
    print(f'correct_dep_args: {correct_dep_args}')


'''
打印结果: 
tool_calls_with_query = [
{'query': '订单123能退款吗', 
'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}}]}}, 

{'query': '订单123能退款吗, 顺便看看物流', 
'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}}, 
                        {'tool': 'get_shipping_status', 'args': {'order_id': '123'}}]}}, 
                        
{'query': '订单123能退款的话 帮我直接退款', 
'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '123'}}, 
                        {'tool': 'create_refund', 'args': {'order_id': '123'}}]}}, 
        
{'query': '订单999能退款吗', 
'tool_call': {'steps': [{'tool': 'check_refund', 'args': {'order_id': '999'}}]}}, 

{'query': 'user u1 的订单123 有没有风险', 
'tool_call': {'steps': [{'tool': 'risk_check', 'args': {}}]}}]
==================================
results: [
{'query': '订单123能退款吗', 
'correctness_tools': True, 
'correctness_llm_args': True, 
'correctness_dep_args': True}, 

{'query': '订单123能退款吗, 顺便看看物流', 
'correctness_tools': True, 
'correctness_llm_args': True, 
'correctness_dep_args': True}, 

{'query': '订单123能退款的话 帮我直接退款', 
'correctness_tools': True, 
'correctness_llm_args': True, 
'correctness_dep_args': True}, 

{'query': '订单999能退款吗', 
'correctness_tools': True, 
'correctness_llm_args': True, 
'correctness_dep_args': True}, 

{'query': 'user u1 的订单123 有没有风险', 
'correctness_tools': True, 
'correctness_llm_args': True, 
'correctness_dep_args': True}]

Process finished with exit code 0
'''


'''
💎我通过evaluation发现：
- LLM在dependency推导上存在问题，
    例如 risk_check缺少get_user，
- 未来可以通过：
    1. 强schema约束
    2. 或自动补step机制
来优化
'''