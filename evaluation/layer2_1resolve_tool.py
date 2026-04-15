from tools.base import Tool
from validators.resolver import resolve_tool

cases = [
    {# Case 1: tool不存在时, 是否返回none
        "case_tool": "check_member_points",
        "expected_name": None,
        "expected_type": None
    },
    {# Case 2: tool存在 且 拼写正确时, 是否可以返回正确tool
        "case_tool": "create_refund",
        "expected_name": "create_refund",
        "expected_type": Tool
    },
    {# Case 3: tool存在 且 拼写轻微错误时, 是否可以返回正确tool
        "case_tool": "chck_refnd",
        "expected_name": "check_refund",
        "expected_type": Tool
    },
    {# Case 4: 与多个 tool 局部相似，但语义不成立，应返回 None
        "case_tool": "check_user_coupon",
        "expected_name": "check_coupon", # ⚠️ 风险
        "expected_type": Tool
    },
    {# Case 5: 多个候选 tool 时的歧义输入
        "case_tool": "refund",
        "expected_name": None,   # 或你也可以定义为 top-1（取决于策略）
        "expected_type": None
    }
]


def evaluate(cases: list):
    results = []
    for case in cases:
        case_tool = case["case_tool"]
        expected_name = case["expected_name"]
        expected_type = case["expected_type"]

        resolved_tool = resolve_tool(case_tool)
        actual_name = resolved_tool.name if resolved_tool else None

        correctness_name = (expected_name == actual_name)
        correctness_type = (isinstance(resolved_tool, expected_type)  # 分支A: 判断是否instance
                            if expected_type else
                            resolved_tool is None  # 分支B: 判断resolved_tool是否为None
                            )

        results.append({"case_tool": case_tool,
                        "expected_tool": expected_name,
                        "actual_tool": resolved_tool.name if resolved_tool else resolved_tool,
                        "expected_type": expected_name,
                        "actual_type": type(resolved_tool).__name__,
                        "correctness_name": correctness_name,
                        "correctness_type": correctness_type
                        },
                       )

    len_cases = len(cases)
    correctness_name = [i["correctness_name"] for i in results]
    correctness_type = [i["correctness_type"] for i in results]

    summary = {"Total cases": len(cases),
               "Name accuracy": sum(correctness_name)/len_cases,
               "Type accuracy": sum(correctness_type)/len_cases, }
    return summary, results


if __name__ == '__main__':
    summary, results = evaluate(cases)
    print(f'results: {results}')
    print(f'summary: {summary}')

'''
results: [
{'case_tool': 'check_member_points', 
'expected_tool': None, 
'actual_tool': None, 
'expected_type': None, 
'resolved_type': 'NoneType', 
'correctness_name': True, 
'correctness_type': True}, 

{'case_tool': 'create_refund', 
'expected_tool': 'create_refund', 
'actual_tool': 'create_refund', 
'expected_type': 'create_refund', 
'resolved_type': 'Tool', 
'correctness_name': True, 
'correctness_type': True}, 

{'case_tool': 'chck_refnd', 
'expected_tool': 'check_refund', 
'actual_tool': 'check_refund', 
'expected_type': 'check_refund', 
'resolved_type': 'Tool', 
'correctness_name': True, 
'correctness_type': True}]


summary: {'Total cases': 3, 'Name accuracy': 1.0, 'Type accuracy': 1.0}

Process finished with exit code 0
'''
