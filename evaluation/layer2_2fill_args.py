from models.order import OrderSummary
from models.refund import RefundEligibility
from tools.registry import tools
from utils.arg_utils import fill_args_from_context


cases = [
    { # Case 1：纯 args（无依赖）
        "case_purpose": "dependency injection",
        "resolved_tool": "create_refund",
        "resolved_args": {"order_id": "123"},
        "tool_results": [RefundEligibility(True, "not shipped")],
        "expected": {"error": False,
                     "params": {"order_id": "123", "eligibility": RefundEligibility}}

    },
    { # Case 2: context 补参数
        "case_purpose": "context fill",
        "resolved_tool": "get_user",
        "resolved_args": {},
        "tool_results": [OrderSummary(order_id="456", user_id="u2", days=4, shipped=False, custom=False, amount=800)],
        "expected": {"error": False,
                     "params": {"user_id": "u2"}}
    },
    { # Case 3: 覆盖 llm args
        "case_purpose": "override llm arg",
        "resolved_tool": "get_user",
        "resolved_args": {"user_id": "WRONG"},
        "tool_results": [OrderSummary(order_id='123', user_id="u1", days=3, shipped=True, custom=False, amount=1000)],
        "expected": {"error": False,
                     "params": {"user_id": "u1"}}
    },
    { # Case 4: 缺 dependency
        "case_purpose": "missing dependency",
        "resolved_tool": "create_refund",
        "resolved_args": {"order_id": "123"},
        "tool_results": [],
        "expected": {"error": True}
    },
    { # Case 5: 多个结果（取最近）
        "case_purpose": "multiple results",
        "resolved_tool": "get_user",
        "resolved_args": {},
        "tool_results": [
            OrderSummary(order_id='123', user_id="u1", days=3, shipped=True, custom=False, amount=1000),
            OrderSummary(order_id="456", user_id="u2", days=4, shipped=False, custom=False, amount=800)
        ],
        "expected": {"error": False,
                     "params": {"user_id": "u2"}}
    }
]
def evaluate(cases: list):
    results = []
    len_cases = len(cases)
    for case in cases:
        resolved_tool = tools[case["resolved_tool"]]
        resolved_args = case["resolved_args"]
        tool_results = case["tool_results"]
        expected= case["expected"]

        correctness_arg_names = True
        correctness_arg_values = True

        try:
            is_error = False
            actual = fill_args_from_context(resolved_tool, resolved_args, tool_results)
        except Exception as e:
            actual = e
            is_error = True

        # 1. error 判断
        correctness_error = (is_error == expected["error"])

        # 2. 仅当不报错时, 才有params, 判断 params
        if not is_error and not expected["error"]:
            expected_params = expected["params"]
            for k, v in expected_params.items():
                # 2.1 key 是否齐全
                if k not in actual:
                    correctness_arg_names = False

                # 2.2 value 判断
                actual_v = actual.get(k)
                if isinstance(v, type):
                    if not isinstance(actual_v, v):
                        correctness_arg_values = False
                else:
                    if actual_v != v:
                        correctness_arg_values = False

        results.append({
            "case_purpose": case["case_purpose"],
            "correctness_error": correctness_error,
            "correctness_arg_names": correctness_arg_names,
            "correctness_arg_values": correctness_arg_values,
            "actual": actual
        })
    error_accuracy = [r["correctness_error"] for r in results]
    arg_name_accuracy = [r['correctness_arg_names'] for r in results]
    arg_value_accuracy = [r['correctness_arg_values'] for r in results]
    summary = {"Total cases": len_cases,
               "error_accuracy": sum(error_accuracy)/len_cases,
               "arg_name_accuracy": sum(arg_name_accuracy)/len_cases,
               "arg_value_accuracy": sum(arg_value_accuracy)/len_cases}
    return summary, results


if __name__ == '__main__':
    summary, results = evaluate(cases)
    print(summary,'\n',results)


'''
summary: 
{'Total cases': 5, 'error_accuracy': 1.0, 'arg_name_accuracy': 1.0, 'arg_value_accuracy': 1.0} 
 
 results: 
 [{'case_purpose': 'dependency injection', 'correctness_error': True, 'correctness_arg_names': True, 'correctness_arg_values': True, 'actual': {'order_id': '123', 'eligibility': RefundEligibility(refundable=True, reason='not shipped')}}, 
 {'case_purpose': 'context fill', 'correctness_error': True, 'correctness_arg_names': True, 'correctness_arg_values': True, 'actual': {'user_id': 'u2'}}, 
 {'case_purpose': 'override llm arg', 'correctness_error': True, 'correctness_arg_names': True, 'correctness_arg_values': True, 'actual': {'user_id': 'u1'}}, 
 {'case_purpose': 'missing dependency', 'correctness_error': True, 'correctness_arg_names': True, 'correctness_arg_values': True, 'actual': ValidationError('missing dependency in tool_results: eligibility')}, 
 {'case_purpose': 'multiple results', 'correctness_error': True, 'correctness_arg_names': True, 'correctness_arg_values': True, 'actual': {'user_id': 'u2'}}]

'''
